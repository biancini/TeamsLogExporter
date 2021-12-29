import sys
import os
import getopt
import configparser
import logging
import functools
from glob import glob
from utils import nearestsunday
from download_json import download_json, zip_jsonfiles
from generate_excel import generate_excel
from upload_excel import upload_excel, upload_zipfile


'''
Scaricare i dati dal report creato appostivamente qui:
https://cqd.teams.microsoft.com/spd/#/Dashboard?language=it-IT
'''


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        logger.debug(f"function {func.__name__} called with args {signature}")
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.exception(f"Exception raised in {func.__name__}. exception: {str(e)}")
            raise e
    return wrapper

class TaskRunner:
    def __init__(self, configuration):
        self.configuration = configuration

    @log
    def run(self):
        pass

class DownloadJsonTask(TaskRunner):
    @log
    def run(self):
        filename = self.configuration['filename']
        logger.info('Downloading all jsons for meeting listed in file %s.', filename)
        numfiles = download_json(self.configuration)
        logger.info('Finished downloading of json files, %d files downloaded.', numfiles)

        if numfiles <= 0:
            raise Exception('No JSON file downloaded!')
        
        return numfiles


class ZipJsonTask(TaskRunner):
    @log
    def run(self):
        logger.info('Zipping all JSON files in zip file %s.', zipfilename)
        zippedfiles = zip_jsonfiles(self.configuration)
        logger.info('Added %d files to zip.', zippedfiles)
    
        if zippedfiles <= 0:
            raise Exception('Error while zipping files.')
        
        return zippedfiles


class UploadAndRemoveZipFileTask(TaskRunner):
    @log
    def run(self):
        sppath = upload_zipfile(self.configuration)
        if sppath is None:
            raise Exception('Zipfile not loaded on Sharepoint.')
        
        logger.info('Loaded zip file to Sharepoint path: %s.', sppath)

        zipfilename = self.configuration['zipfile']
        os.remove(zipfilename)

        return 1

class GenerateExcelFilesAndRemoveJsonTask(TaskRunner):
    @log
    def run(self):
        numexcels = generate_excel(self.configuration)

        if numexcels <= 0:
            raise Exception('No excels generated.')
        
        logging.info('Creati %d files.', numexcels)

        # Remove all json files downloaded
        basedir = 'json/'
        files = glob(f'{basedir}**/*.json', recursive=True)
        for f in files:
            os.remove(f)

        return numexcels


class UploadAndRemoveExcelFilesTask(TaskRunner):
    @log
    def run(self):
        total_files, file_uploaded = upload_excel(self.configuration)
        logging.info('Uploaded to Sharepoint %d files.', file_uploaded)

        if file_uploaded <= 0:
            raise Exception(f'Should have uploaded {total_files} files, but uploaded {file_uploaded}.')

        # Remove all excel files created
        basedir = 'excel/'
        files = glob(f'{basedir}**/*.xlsx', recursive=True)
        for f in files:
            os.remove(f)
        
        return file_uploaded


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('configuration.ini')
    ente = 'ENAIP'
    filename = 'calls.csv'
    zipfilename = '%s_Report.zip' % nearestsunday().strftime("%Y-%m-%d")

    try:
        opts, _ = getopt.getopt(sys.argv[1:], "he:f:z:", ["help", "ente=", "file=", "zipfile="])
    except getopt.GetoptError:
        logger.info('download_json.py [-e <ente>] [-f <file>] [-z <zipfile>]')
        sys.exit(2)
    
    for o, a in opts:
        if o in ('-h', '--help'):
            logger.info('download_reports.py [-e <ente>] [-f <file>] [-z <zipfile>]')
            sys.exit()
        elif o in ('-e', '--ente'):
            ente = a.upper()
        elif o in ('-f', '--file'):
            filename = a
        elif o in ('-z', '--zipfile'):
            zipfilename = a
        else:
            assert False

    configuration = config[ente]
    configuration['ente'] = ente
    configuration['filename'] = filename
    configuration['zipfile'] = zipfilename
    configuration['local'] = 'false'

    logger.info('Working for institution %s.', ente)

    for a in [
            DownloadJsonTask(configuration),
            ZipJsonTask(configuration),
            UploadAndRemoveZipFileTask(configuration),
            GenerateExcelFilesAndRemoveJsonTask(configuration),
            UploadAndRemoveExcelFilesTask(configuration),
        ]:
        a.run()

    logger.info('Script finito.')