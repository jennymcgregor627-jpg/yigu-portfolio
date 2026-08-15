## 忆古 — 线路二：视觉 — 文物背景墙

### 项目背景

忆古的 Hero 页需要一个有沉浸感的背景——一面由古代真实器物图片平铺而成的"文物墙"。浏览者第一眼看到这面墙时，应该感受到一种朦胧的、若隐若现的历史质感，仿佛站在博物馆的暗厅里，隔着玻璃望向馆藏。

### 当前状态（截至 2026-08-10）

**已有结构**：
- Hero 区域 `.hero`（100vh，`background: var(--bg-deep) #0A0806`）
- 一个 8×6 的 CSS Grid：`.hero-grid-bg`（`z-index: 2`）
- 48 个 `.grid-tile` 格子，用 JS 的 `wall()` 函数填充背景图
- 图片来源：`bronze-wall/b1.jpg` ~ `bronze-wall/b11.jpg`（共 10 张，600px 宽度，源自 Unsplash 搜索下载）

**CSS 设置**：
```css
.grid-tile {
    background-size: cover; background-position: center;
    opacity: 0.35;
    filter: blur(2px) brightness(1.6) sepia(0.4);
}
```

**Hero 层叠结构**：
```
z-index: 1  — hero-bg-layer（光环、金线）
z-index: 2  — hero-grid-bg（文物墙）← 在这里
z-index: 3  — scroll-hint
z-index: 4  — hero-content（文字、搜索框）
```

### 当前问题

1. **背景墙不可见或极难看到**：`opacity: 0.35` 叠加在 `#0A0806` 深色背景上几乎等于没有。之前多次尝试调参都未能彻底解决。
2. **图片内容不匹配**：`bronze-wall/` 下的图片来自 Unsplash 搜索，可能混入了人物自拍、现代场景等非文物内容，与"青铜器/古文物"的主题不符。
3. **只有一套滤镜逻辑**：当前的 opacity+blur+brightness+sepia 组合过于粗暴——要么太暗看不到，要么太亮破坏氛围。

### 目标

一面在深色背景上**肉眼清晰可辨**的文物图片墙，带有朦胧感和古青铜色调，鼠标移过时有微弱的"手电筒扫过壁画"效果。

---

## 开发计划

### 第一阶段：图片资产重建（最关键）

**问题**：现有的 `bronze-wall/` 图片（来自 Unsplash）内容不可控，可能不是真正文物。

**方案**：使用 AI 图片生成工具，按统一规格生成真实古代器物图片。

**具体任务**：

1. 创建新目录 `artifact-wall/`
2. 生成 15 张图片，内容为以下古代器物（每张 600×600，深色背景，单一器物居中）：
   - 青铜鼎、青瓷碗、玉琮、陶俑、唐三彩马、铜镜
   - 战国漆器、铁剑、彩陶罐、编钟、铜爵
   - 博山炉、银壶、石狮、玉佩
3. 图片风格要求：
   - 博物馆藏品摄影风格，侧光打亮器物轮廓
   - 深褐色/黑色背景
   - 器物本身颜色保留真实感（青铜锈绿、陶瓷青白、玉的温润）
4. 统一命名为 `w01.jpg` ~ `w15.jpg`

**涉及文件**：新建 `yigu-preview/artifact-wall/` 目录及图片文件；修改 `index.html` 中 `wall()` 函数的图片路径

**验收标准**：打开 `artifact-wall/` 目录，15 张图片都是文物主体清晰、背景深色的博物馆风格照片。

---

### 第二阶段：CSS 可见性重做

**核心思路**：放弃当前的 opacity+filter 方案。图片以正常亮度渲染，通过叠加层实现朦胧感。

**具体任务**：

1. **去掉 `.grid-tile` 的 `opacity` 和 `filter`**，改为：
   ```css
   .grid-tile {
       background-size: cover; background-position: center;
       filter: none;
       opacity: 1;
   }
   ```

2. **每个格子添加内层遮罩**：
   - 在 `.hero-grid-bg` 上用一个 `::after` 伪元素覆盖整面墙
   - `background: rgba(10,8,6, 0.6)` — 半透明黑色叠加，压暗整面墙
   - 叠加层添加 `backdrop-filter: blur(1.5px)` — 在层叠上下文中实现朦胧

3. **色调统一**：
   - `.hero-grid-bg` 整面墙再叠加一层：
   ```css
   filter: sepia(0.3) hue-rotate(-10deg) saturate(0.7);
   ```
   - 把所有图片色调统一拉向青铜锈绿 + 暗金方向

4. **自动漂浮动画**：
   - 给 `.hero-grid-bg` 一个极慢的 `@keyframes` 循环
   - `transform: translate(0,0)` → `translate(-15px,-8px)` → `translate(0,0)`
   - 8 秒一个周期，`ease-in-out`
   - 营造"壁画在缓慢呼吸"的感觉

**涉及文件**：`yigu-preview/index.html`（CSS 部分）

**验收标准**：
- 打开页面，Hero 背景墙清晰可见
- 图片有朦胧感但不至于完全模糊
- 整体色调偏青铜锈绿/暗金
- 墙面在缓慢微移

---

### 第三阶段：交互微光（手电筒效果）

**核心思路**：鼠标在 Hero 区域移动时，离鼠标最近的格子微微变亮，像手电筒扫过壁画。

**具体任务**：

1. 给 `.hero-grid-bg` 的 `::after` 遮罩层添加 CSS 变量控制：
   ```css
   --light-x: 50%;
   --light-y: 50%;
   ```
2. 将遮罩层改为 `radial-gradient` 而非纯色：
   ```css
   background: radial-gradient(
       circle 300px at var(--light-x) var(--light-y),
       rgba(10,8,6, 0.2) 0%,
       rgba(10,8,6, 0.6) 60%,
       rgba(10,8,6, 0.75) 100%
   );
   ```
   - 中心（鼠标位置）透明，边缘更暗，制造"局部照亮"效果
3. 用节流的 `mousemove` 事件监听 Hero 区域，更新 CSS 变量
4. 鼠标离开 Hero 区域时，`--light-x/--light-y` 平滑回到中心（CSS transition 1.5s）

**涉及文件**：`yigu-preview/index.html`（CSS + JS）

**验收标准**：鼠标在 Hero 上移动，墙面在鼠标位置附近微微变亮。

---

### 第四阶段：细调与多端适配

**具体任务**：

1. 移动端优化：
   - 移动端无 hover，去掉手电筒效果，改为整面墙更亮的默认状态
   - 缩小 gap 到 1px，保持网格密度
2. 网格间隙金线：
   ```css
   .hero-grid-bg {
       gap: 1px;
       background: rgba(201,169,110, 0.08);
   }
   ```
   - 格子在间隙处露出极细的金色底线
3. 在浏览器中反复验证可见度，必要时微调遮罩的 alpha 和 blur 值

**涉及文件**：`yigu-preview/index.html`

**验收标准**：
- 桌面端效果完整（手电筒 + 漂浮 + 青铜色调）
- 移动端（<768px）墙面明亮可见、无性能问题
- 黄金分隔线隐约可见

---

## 阶段依赖关系

```
第一阶段（图片重建）→ 第二阶段（CSS 重做）→ 第三阶段（手电筒效果）→ 第四阶段（细调适配）
```

第一阶段是整个视觉线路的基础——没有正确的图片，后面的滤镜和交互都是空中楼阁。

---

## 技术注意事项

- 所有代码在一个 HTML 文件中（内嵌 CSS + JS）
- 15 张图片的 base64 不应嵌入 HTML（会导致文件过大），使用本地文件路径引用
- 手电筒效果需要 `requestAnimationFrame` + 节流，确保 60fps
- 移动端（`pointer: coarse`）自动禁用 mousemove 监听
- `backdrop-filter` 在部分浏览器上可能有性能问题，备选方案是纯 CSS 的 `mask-image: radial-gradient`
