# Export every slide to PNG with the installed PowerPoint and dump the text extents
# PowerPoint itself measures (TextFrame2.TextRange.Bound*). Called by render_review.py.
param(
  [Parameter(Mandatory)][string]$Pptx,
  [Parameter(Mandatory)][string]$OutDir,
  [string]$Prefix = 'slide',
  [int]$Width = 1600,
  [string]$AuditJson = ''
)
$ErrorActionPreference = 'Stop'
$pptxPath = (Resolve-Path $Pptx).Path
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$outPath = (Resolve-Path $OutDir).Path

function Get-TextShapes($shapes) {
  foreach ($s in $shapes) {
    if ($s.Type -eq 6) { Get-TextShapes $s.GroupItems; continue }   # msoGroup
    try {
      if ($s.HasTextFrame -and $s.TextFrame2.HasText -and $s.Rotation -eq 0) {
        $r = $s.TextFrame2.TextRange
        [pscustomobject]@{
          text = ($r.Text -replace "[`r`n\x0b]", ' ').Trim()
          frame = @($s.Left, $s.Top, $s.Width, $s.Height)
          bound = @($r.BoundLeft, $r.BoundTop, $r.BoundWidth, $r.BoundHeight)
          wrap = [bool]$s.TextFrame2.WordWrap
        }
      }
    } catch { }   # charts, OLE objects, SmartArt
  }
}

$app = New-Object -ComObject PowerPoint.Application
$hadOpen = $app.Presentations.Count
try {
  $pres = $app.Presentations.Open($pptxPath, $true, $false, $false)   # read-only, untitled, no window
  $sw = $pres.PageSetup.SlideWidth; $sh = $pres.PageSetup.SlideHeight
  $h = [int][math]::Round($Width * $sh / $sw)
  $slides = @()
  foreach ($s in $pres.Slides) {
    $s.Export((Join-Path $outPath ("{0}-{1:D2}.png" -f $Prefix, $s.SlideIndex)), 'PNG', $Width, $h)
    if ($AuditJson) { $slides += ,@{ slide = $s.SlideIndex; shapes = @(Get-TextShapes $s.Shapes) } }
  }
  $pres.Close()
  if ($AuditJson) {
    $json = @{ slide_w = $sw; slide_h = $sh; slides = $slides } | ConvertTo-Json -Depth 6
    [IO.File]::WriteAllText($AuditJson, $json, (New-Object Text.UTF8Encoding $false))
  }
} finally {
  if ($hadOpen -eq 0 -and $app.Presentations.Count -eq 0) { $app.Quit() }
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
