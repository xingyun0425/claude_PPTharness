"""Synthetic integration fixture, never a paper presentation or design template."""
import sys
import build_deck_template as builder

builder.THEME = {"colors": {"navy": "663C55", "blue": "287C79", "text": "25333B",
                            "pale": "F2EAF0", "line": "D8C9D3", "grey": "62717B"},
                 "font": "Microsoft YaHei",
                 "icons": {"fixture": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="#287C79"/></svg>'}}


@builder.slide
def components(cv, number):
    cv.title("技术验证：原生组件与 SVG")
    cv.text("此页使用合成内容，仅用于验证生成流程", 84, 155, pt=18)
    g = cv.group("可编辑说明")
    g.card(84, 240, 800, 220)
    g.text("文字与卡片可分别编辑", 124, 300, pt=24, bold=True)
    g.para("SVG 作为独立图形嵌入，标签保持原生文本。", 124, 355, 700, pt=18)
    cv.icon_c("fixture", 1150, 340, 160)
    cv.text("SVG + PNG 后备图", 1150, 470, pt=18, align="c")
    cv.arrow(900, 340, 1025, 340)
    return "Source: synthetic integration fixture. No research claims or measured results."


@builder.slide
def evidence(cv, number):
    cv.title("技术验证：原生表格与折线图")
    cv.text("合成数据，无科研含义", 84, 155, pt=18)
    cv.table(84, 240, [200, 160], ["项目", "数值"], [["A", "10"], ["B", "15"], ["C", "12"]], row_h=70, head_h=70, pt=18, head_pt=18)
    cv.line_chart(560, 230, 940, 490, ["A", "B", "C"], [("Synthetic", [10, 15, 12], "287C79", False)], 20, major=5, pt=16)
    return "Source: synthetic values A=10, B=15, C=12. For editable chart and table checks only."


if __name__ == "__main__":
    builder.main()
