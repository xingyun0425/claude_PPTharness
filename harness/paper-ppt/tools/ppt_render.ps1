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

function Get-Shapes($shapes) {
  # Every leaf shape in drawing order (later = on top): text extents and lines for text
  # shapes, plus each box's kind and fill/outline so the audit can see text a box hides.
  foreach ($s in $shapes) {
    if ($s.Type -eq 6) { Get-Shapes $s.GroupItems; continue }   # msoGroup
    $script:z += 1
    $item = [ordered]@{ z = $script:z; name = $s.Name; type = [int]$s.Type;
                        frame = @($s.Left, $s.Top, $s.Width, $s.Height); filled = $false; transp = 0.0; outlined = $false; auto = -1 }
    try { $item.filled = [bool]($s.Fill.Visible -ne 0); $item.transp = [double]$s.Fill.Transparency } catch { }
    try { $item.outlined = [bool]($s.Line.Visible -ne 0) } catch { }
    try { if ($s.Type -eq 1) { $item.auto = [int]$s.AutoShapeType } } catch { }
    if ($s.Type -in 3, 13, 28 -or $s.HasTable -or $s.HasChart) { $item.filled = $true }   # chart, picture, graphic, table
    try {
      if ($s.HasTextFrame -and $s.TextFrame2.HasText -and $s.Rotation -eq 0) {
        $r = $s.TextFrame2.TextRange
        $lines = @()
        $n = $r.Lines().Count
        for ($i = 1; $i -le $n; $i++) { $lines += ($r.Lines($i, 1).Text -replace "[`r`n\x0b]", '') }
        $item.text = ($r.Text -replace "[`r`n\x0b]", ' ').Trim()
        $item.bound = @($r.BoundLeft, $r.BoundTop, $r.BoundWidth, $r.BoundHeight)
        $item.wrap = [bool]$s.TextFrame2.WordWrap
        $item.lines = $lines
      }
    } catch { }   # charts, OLE objects, SmartArt
    [pscustomobject]$item
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
    if ($AuditJson) {
      $script:z = 0
      $items = @(Get-Shapes $s.Shapes)
      $slides += ,@{ slide = $s.SlideIndex; shapes = @($items | Where-Object { $_.text }); items = $items }
    }
  }
  $pres.Close()
  if ($AuditJson) {
    $json = @{ slide_w = $sw; slide_h = $sh; slides = $slides } | ConvertTo-Json -Depth 8
    [IO.File]::WriteAllText($AuditJson, $json, (New-Object Text.UTF8Encoding $false))
  }
} finally {
  if ($hadOpen -eq 0 -and $app.Presentations.Count -eq 0) { $app.Quit() }
  [System.Runtime.InteropServices.Marshal]::ReleaseComObject($app) | Out-Null
}
