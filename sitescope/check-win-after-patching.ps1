# $hf = Get-HotFix | Sort-Object -Descending -Property InstalledOn
$hf = Get-WindowsPackage -Online | Sort-Object -Descending -Property InstallTime

foreach ($h in $hf) {
    $d = $($h.InstallTime).ToString()
    $state = $($h.PackageState)
    Write-Host "$d => $state"
}