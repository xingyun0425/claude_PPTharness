# Export each slide of a PPTX to PNG using the installed PowerPoint (for visual checks).
param([Parameter(Mandatory)][string]$Pptx, [Parameter(Mandatory)][string]$OutDir, [int]$Width = 2400)
$ErrorActionPreference = 'Stop'
$pptxPath = (Resolve-Path $Pptx).Path
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$outPath = (Resolve-Path $OutDir).Path
$app = New-Object -ComObject PowerPoint.Application
try {
  $pres = $app.Presentations.Open($pptxPath, $true, $false, $false)  # read-only, untitled, no window
  $h = [int]($Width * $pres.PageSetup.SlideHeight / $pres.PageSetup.SlideWidth)
  foreach ($s in $pres.Slides) {
    $s.Export((Join-Path $outPath ("slide-{0:D2}.png" -f $s.SlideIndex)), 'PNG', $Width, $h)
  }
  $pres.Close()
} finally {
  $app.Quit()
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
Get-ChildItem $outPath -Filter *.png | ForEach-Object { $_.Name }
