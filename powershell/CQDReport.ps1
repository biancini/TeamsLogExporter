function Get-CQDToken ([string]$client_id){
  $resourceUrl = $WebResource
  Add-Type -AssemblyName System.Web
  $redirectUrl = "https://cqd.teams.microsoft.com/spd/"
  $nonce = [guid]::NewGuid().GUID
  $url = "https://login.microsoftonline.com/common/oauth2/authorize?response_type=token&redirect_uri=" +
  [System.Web.HttpUtility]::UrlEncode($redirectUrl) +
  "&client_id=$client_id" +
  "&prompt=login" + "&nonce=$nonce" + "&resource=" + [System.Web.HttpUtility]::UrlEncode($WebResource)

  Add-Type -AssemblyName System.Windows.Forms

  $form = New-Object -TypeName System.Windows.Forms.Form -Property @{ Width = 440; Height = 640 }
  $web = New-Object -TypeName System.Windows.Forms.WebBrowser -Property @{ Width = 420; Height = 600; Url = ($url) }
  $DocComp = {
    $Global:uri = $web.Url.AbsoluteUri
    if ($Global:Uri -match "error=[^&]*|access_token=[^&]*") {$form.Close()}
  }

  $	.ScriptErrorsSuppressed = $true
  $web.Add_DocumentCompleted($DocComp)
  $form.Controls.Add($web)
  $form.Add_Shown({$form.Activate()})
  $form.ShowDialog() | Out-Null

  $Script:TokenLifeTime = [Web.HttpUtility]::ParseQueryString(($web.Url -replace '^.*?(expires_in.+)$','$1'))['expires_in']
  $Script:Token = [Web.HttpUtility]::ParseQueryString(($web.Url -replace '^.*?(access_token.+)$','$1'))['access_token']
  
  return ('Bearer {0}' -f $Script:Token)
}

$configRest = Invoke-RestMethod -Uri "https://cqd.teams.microsoft.com/repository/clientconfiguration" -Method Get -SessionVariable WebSession -UserAgent "CQDPowerShell V2.0"
$WebResource = $configRest.AuthLoginResource
$AADBearerToken = Get-CQDToken $configRest.AuthWebAppClientId
$WebSession.headers.Add('Authorization',$AADBearerToken)
Write-Output $AADBearerToken

<# Uncomment this block to see Dimensions and Measurements available
$CubeRequest = Invoke-WebRequest -Uri 'https://cqd.teams.microsoft.com/data/noam/CubeStructure' -WebSession $WebSession -Method Get -UserAgent "CQDPowerShell V2.0"
$List = ConvertFrom-Json $CubeRequest
$Dimensions = $List.Dimensions
$Measurements = $List.Measurements
$arrDimensionsAvailable = [System.Collections.ArrayList]@()
$arrMeasuresAvailable = [System.Collections.ArrayList]@()
foreach($Dimension in $Dimensions){
    foreach($attribute in $Dimension.Attributes){$arrDimensionsAvailable.Add($attribute) | Out-Null}
}
foreach($Measurement in $Measurements){
    foreach($attribute in $Measurement.Attributes){$arrMeasuresAvailable.Add($attribute) | Out-Null}
}
#>

$query = @'
{
    "Filters":[
        {"DataModelName":"[AllStreams].[Date]","Caption":"NA","Value":"[2020-11-09],[2020-11-10],[2020-11-12],[2020-11-11],[2020-11-13],[2020-11-14],","Operand":0,"UnionGroup":""}
    ],
    "Dimensions":[
        {"DataModelName":"[AllStreams].[Meeting Id]"}
    ],
    "Measurements":[
        {"DataModelName":"[Measures].[Avg Call Duration]"}
    ],
    LimitResultRowsCount:200000
}
'@

$IRM = Invoke-RestMethod -Uri 'https://cqd.teams.microsoft.com/data/noam/RunQuery' -WebSession $WebSession -Method Post -Body $Query -ContentType 'application/json' -UserAgent "CQDPowerShell V2.0"

$headers = @()
$queryDeJsonified = $query | ConvertFrom-Json
foreach($queryDimension in $queryDeJsonified.Dimensions){$headers += $queryDimension.DataModelName}
foreach($queryMeasurement in $queryDeJsonified.Measurements){$headers += $queryMeasurement.DataModelName}
$headersCount = $headers.Count

$arrQueryResults = [System.Collections.ArrayList]@()
foreach($record in $IRM.DataResult){
    $workingObject = [PSCustomObject]@{}
    for($i=0;$i -lt $headersCount;$i++){$workingObject | Add-Member -MemberType NoteProperty -Name $headers[$i] -Value $record[$i]}
    $arrQueryResults.Add($workingObject) | Out-Null
}

Write-Output "Fine."