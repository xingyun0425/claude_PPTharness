"""
AI Recursive Self-Improvement Domain Icons
领域专用图标库 - 线性轮廓风格（stroke-based）

Style Guide:
- 线宽：1.5-2pt
- 描边颜色：#3B82F6（亮蓝）
- 填充颜色：#E0E7FF（浅蓝紫）或none
- 尺寸：viewBox="0 0 100 100"，实际放置时缩放到30-80px
- 无圆形背景，直接放置
"""

ICONS = {
    # 神经网络节点 - 3x3网格连线
    'neural-net': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#3B82F6" stroke-width="1.5" fill="none">
    <!-- 连接线（背景层）-->
    <line x1="25" y1="25" x2="50" y2="50" />
    <line x1="75" y1="25" x2="50" y2="50" />
    <line x1="25" y1="75" x2="50" y2="50" />
    <line x1="75" y1="75" x2="50" y2="50" />
    <line x1="50" y1="25" x2="50" y2="75" />
    <line x1="25" y1="50" x2="75" y2="50" />
  </g>
  <g fill="#E0E7FF" stroke="#3B82F6" stroke-width="2">
    <!-- 节点（前景层）-->
    <circle cx="25" cy="25" r="6" />
    <circle cx="50" cy="25" r="6" />
    <circle cx="75" cy="25" r="6" />
    <circle cx="25" cy="50" r="6" />
    <circle cx="50" cy="50" r="8" />
    <circle cx="75" cy="50" r="6" />
    <circle cx="25" cy="75" r="6" />
    <circle cx="50" cy="75" r="6" />
    <circle cx="75" cy="75" r="6" />
  </g>
</svg>''',

    # 循环箭头 - self-improvement核心视觉
    'loop-arrow': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowhead-loop" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto">
      <polygon points="0 0, 10 3, 0 6" fill="#3B82F6" />
    </marker>
  </defs>
  <path d="M 70 30 A 25 25 0 1 1 30 30"
        stroke="#3B82F6" stroke-width="2.5" fill="none"
        marker-end="url(#arrowhead-loop)" />
  <path d="M 30 70 A 25 25 0 1 1 70 70"
        stroke="#3B82F6" stroke-width="2.5" fill="none"
        marker-end="url(#arrowhead-loop)" />
  <circle cx="50" cy="50" r="12" fill="#E0E7FF" stroke="#3B82F6" stroke-width="2" />
</svg>''',

    # 验证器盾牌 - 带勾标记
    'verifier-shield': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <path d="M 50 10 L 80 25 L 80 55 Q 80 75, 50 90 Q 20 75, 20 55 L 20 25 Z"
        fill="#E0E7FF" stroke="#3B82F6" stroke-width="2" />
  <polyline points="35 50, 45 60, 65 35"
            stroke="#3B82F6" stroke-width="3" fill="none"
            stroke-linecap="round" stroke-linejoin="round" />
</svg>''',

    # 训练齿轮 - 表示训练过程
    'training-gear': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <g fill="#E0E7FF" stroke="#3B82F6" stroke-width="2">
    <circle cx="50" cy="50" r="18" />
    <!-- 8个齿 -->
    <rect x="48" y="15" width="4" height="12" />
    <rect x="70" y="27" width="12" height="4" transform="rotate(45 76 29)" />
    <rect x="73" y="48" width="12" height="4" />
    <rect x="70" y="69" width="12" height="4" transform="rotate(-45 76 71)" />
    <rect x="48" y="73" width="4" height="12" />
    <rect x="18" y="69" width="12" height="4" transform="rotate(45 24 71)" />
    <rect x="15" y="48" width="12" height="4" />
    <rect x="18" y="27" width="12" height="4" transform="rotate(-45 24 29)" />
  </g>
  <circle cx="50" cy="50" r="10" fill="white" stroke="#3B82F6" stroke-width="2" />
</svg>''',

    # 部署火箭 - 表示deployment
    'deployment-rocket': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <g fill="#E0E7FF" stroke="#3B82F6" stroke-width="2">
    <!-- 火箭主体 -->
    <path d="M 50 15 L 60 40 L 60 70 L 50 75 L 40 70 L 40 40 Z" />
    <!-- 窗口 -->
    <circle cx="50" cy="35" r="6" fill="white" />
    <!-- 尾翼 -->
    <path d="M 40 55 L 30 65 L 40 70 Z" />
    <path d="M 60 55 L 70 65 L 60 70 Z" />
    <!-- 火焰 -->
    <path d="M 45 75 L 40 85 L 45 80 L 50 90 L 55 80 L 60 85 L 55 75 Z"
          fill="#F97316" stroke="none" />
  </g>
</svg>''',

    # 数据流管道
    'data-flow': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrowhead-flow" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <polygon points="0 0, 8 3, 0 6" fill="#3B82F6" />
    </marker>
  </defs>
  <g stroke="#3B82F6" stroke-width="2" fill="none">
    <path d="M 15 30 Q 50 20, 85 30" marker-end="url(#arrowhead-flow)" />
    <path d="M 15 50 L 85 50" marker-end="url(#arrowhead-flow)" />
    <path d="M 15 70 Q 50 80, 85 70" marker-end="url(#arrowhead-flow)" />
  </g>
  <circle cx="15" cy="30" r="5" fill="#E0E7FF" stroke="#3B82F6" stroke-width="2" />
  <circle cx="15" cy="50" r="5" fill="#E0E7FF" stroke="#3B82F6" stroke-width="2" />
  <circle cx="15" cy="70" r="5" fill="#E0E7FF" stroke="#3B82F6" stroke-width="2" />
</svg>''',

    # 法槌 - 表示judge/评估
    'judge-gavel': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <g fill="#E0E7FF" stroke="#3B82F6" stroke-width="2">
    <!-- 槌头 -->
    <rect x="50" y="20" width="35" height="15" rx="3" />
    <!-- 槌柄 -->
    <rect x="60" y="35" width="6" height="35" />
    <!-- 底座 -->
    <rect x="20" y="75" width="60" height="10" rx="2" />
  </g>
</svg>''',

    # 研究烧瓶 - 表示research/实验
    'research-flask': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <g fill="none" stroke="#3B82F6" stroke-width="2">
    <!-- 烧瓶颈 -->
    <line x1="40" y1="20" x2="40" y2="35" />
    <line x1="60" y1="20" x2="60" y2="35" />
    <line x1="38" y1="20" x2="62" y2="20" />
    <!-- 烧瓶体 -->
    <path d="M 40 35 L 25 70 Q 25 80, 35 85 L 65 85 Q 75 80, 75 70 L 60 35 Z"
          fill="#E0E7FF" />
    <!-- 液体 -->
    <path d="M 42 45 L 30 68 Q 30 75, 37 78 L 63 78 Q 70 75, 70 68 L 58 45 Z"
          fill="#60A5FA" stroke="none" />
  </g>
</svg>''',

    # 金字塔层级 - verification hierarchy
    'hierarchy-pyramid': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <g stroke="#3B82F6" stroke-width="1.5">
    <!-- 五层金字塔 -->
    <path d="M 50 15 L 65 30 L 35 30 Z" fill="#1E3A8A" />
    <path d="M 35 30 L 70 45 L 30 45 Z" fill="#3B82F6" />
    <path d="M 30 45 L 75 60 L 25 60 Z" fill="#60A5FA" />
    <path d="M 25 60 L 80 75 L 20 75 Z" fill="#93C5FD" />
    <path d="M 20 75 L 85 90 L 15 90 Z" fill="#DBEAFE" />
  </g>
</svg>''',

    # AI Agent机器人（简化线性版）
    'agent-robot': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <g fill="#E0E7FF" stroke="#3B82F6" stroke-width="2">
    <!-- 头部 -->
    <rect x="35" y="25" width="30" height="25" rx="5" />
    <!-- 眼睛 -->
    <circle cx="43" cy="35" r="3" fill="#3B82F6" />
    <circle cx="57" cy="35" r="3" fill="#3B82F6" />
    <!-- 天线 -->
    <line x1="50" y1="20" x2="50" y2="25" stroke="#3B82F6" stroke-width="2" />
    <circle cx="50" cy="18" r="3" />
    <!-- 身体 -->
    <rect x="30" y="50" width="40" height="30" rx="3" />
    <!-- 胸前显示屏 -->
    <rect x="40" y="58" width="20" height="12" rx="1" fill="white" />
    <!-- 手臂 -->
    <rect x="20" y="55" width="10" height="4" />
    <rect x="70" y="55" width="10" height="4" />
    <!-- 腿 -->
    <rect x="38" y="80" width="8" height="12" />
    <rect x="54" y="80" width="8" height="12" />
  </g>
</svg>''',

    # 警告标志（用于失败模式）
    'warning-sign': '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <g fill="#FEE2E2" stroke="#C00000" stroke-width="2.5">
    <path d="M 50 15 L 85 80 L 15 80 Z" />
  </g>
  <text x="50" y="65" font-size="40" font-weight="bold"
        text-anchor="middle" fill="#C00000">!</text>
</svg>''',
}

# 导出为模块级变量供 build_deck.py 导入
__all__ = ['ICONS']
