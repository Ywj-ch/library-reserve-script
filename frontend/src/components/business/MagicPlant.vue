<template>
  <div 
    v-if="!isMobile"
    class="magic-plant-container"
    @mouseenter="handleInteraction"
    @click="handleInteraction"
  >
    <object
      ref="plantSvg"
      :data="svgUrl"
      type="image/svg+xml"
      class="magic-plant"
      @load="initializePlant"
    ></object>
    
    <Transition name="fade">
      <div v-if="showBlessing" class="blessing-tooltip">
        {{ currentBlessing }}
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { gsap } from 'gsap'

const plantSvg = ref<HTMLElement | null>(null)
const showBlessing = ref(false)
const currentBlessing = ref('')
const isMobile = ref(false)
const svgUrl = '/plant.svg'

const blessings = [
  '今日份的好运已送达 ✨',
  '愿你拥有美好的一天 🌸',
  '坚持就是胜利 🌱',
  '阳光总会照进来 ☀️',
  '相信自己，你可以的 💪',
  '每一天都是新的开始 🌅',
  '慢慢来，好戏都在烟火里 🎆',
  '保持热爱，奔赴山海 ⛰️',
  '生活明朗，万物可爱 🌈',
  '今天也要加油鸭 🦆',
  '心有猛虎，细嗅蔷薇 🌹',
  '平凡的日子也在发光 ✨',
  '你笑起来真好看 😊',
  '世界因你而精彩 🌍',
  '做自己的小太阳 🌻',
]

let isAnimating = false
let svgDoc: Document | null = null
let cooldownTimeout: number | null = null

function checkMobile() {
  isMobile.value = window.innerWidth <= 768
}

function initializePlant() {
  const obj = plantSvg.value as HTMLObjectElement
  if (!obj || !obj.contentDocument) return
  
  svgDoc = obj.contentDocument
}

function getRandomLeaves() {
  if (!svgDoc) return []
  
  const allLeaves = Array.from(svgDoc.querySelectorAll('.plant-leaf'))
  const count = Math.floor(Math.random() * 3) + 1 // 1-3片
  const shuffled = allLeaves.sort(() => Math.random() - 0.5)
  
  return shuffled.slice(0, count)
}

function createFallingLeaf(originalLeaf: Element) {
  if (!svgDoc) return null
  
  const leafGroup = originalLeaf.cloneNode(true) as SVGGElement
  const fallingLeavesGroup = svgDoc.querySelector('#falling-leaves')
  
  if (!fallingLeavesGroup) return null
  
  leafGroup.removeAttribute('class')
  leafGroup.classList.add('falling-leaf')
  fallingLeavesGroup.appendChild(leafGroup)
  
  return leafGroup
}

function handleInteraction() {
  if (isAnimating || !svgDoc) return
  
  isAnimating = true
  currentBlessing.value = blessings[Math.floor(Math.random() * blessings.length)]
  showBlessing.value = false
  
  const timeline = gsap.timeline({
    onComplete: () => {
      isAnimating = false
    }
  })
  
  // ===== 1. 风效果（0.0-0.5s） =====
  const windEffect = svgDoc.querySelector('#wind-effect') as SVGGElement
  const windLines = svgDoc.querySelectorAll('[id^="wind-line"]')
  
  timeline.to(windEffect, {
    duration: 0.1,
    opacity: 1,
    ease: 'power2.out'
  }, 0)
  
  windLines.forEach((line, index) => {
    const delay = index * 0.05
    
    timeline.to(line, {
      duration: 0.4,
      x: 200,
      ease: 'power2.in',
      onComplete: () => {
        gsap.set(line, { x: 0 })
      }
    }, delay)
  })
  
  timeline.to(windEffect, {
    duration: 0.1,
    opacity: 0,
    ease: 'power2.out'
  }, 0.5)
  
  // ===== 2. 植株摇摆（0.1-0.8s） =====
  const stemGroup = svgDoc.querySelector('#stem-group') as SVGGElement
  const allLeaves = Array.from(svgDoc.querySelectorAll('.plant-leaf'))
  
  // 茎向右弯曲
  timeline.to(stemGroup, {
    duration: 0.3,
    rotation: 8,
    transformOrigin: 'center bottom',
    ease: 'power2.out'
  }, 0.1)
  
  // 所有叶子跟随摆动
  allLeaves.forEach((leaf, index) => {
    const delay = 0.1 + index * 0.02
    
    timeline.to(leaf, {
      duration: 0.25,
      rotation: 12,
      transformOrigin: 'left center',
      ease: 'power2.out'
    }, delay)
  })
  
  // ===== 3. 落叶效果（0.2-2.0s） =====
  const fallingLeaves = getRandomLeaves()
  
  fallingLeaves.forEach((leaf, index) => {
    const fallingLeaf = createFallingLeaf(leaf)
    if (!fallingLeaf) return
    
    const endX = 100 + Math.random() * 60
    const endY = 180 + Math.random() * 20
    const rotation = 360 + Math.random() * 360
    
    // 落叶飘落
    timeline.fromTo(fallingLeaf,
      {
        x: 0,
        y: 0,
        rotation: 0,
        opacity: 1,
        scale: 1
      },
      {
        duration: 1.5 + Math.random() * 0.5,
        x: endX,
        y: endY,
        rotation: rotation * (Math.random() > 0.5 ? 1 : -1),
        opacity: 0,
        scale: 0.6,
        ease: 'power1.in',
        onComplete: () => {
          if (fallingLeaf.parentNode) {
            fallingLeaf.parentNode.removeChild(fallingLeaf)
          }
        }
      },
      0.2 + index * 0.1
    )
    
    // 隐藏原始叶子
    timeline.to(leaf, {
      duration: 0.1,
      opacity: 0
    }, 0.2 + index * 0.1)
    
    // 恢复原始叶子
    timeline.to(leaf, {
      duration: 0.4,
      opacity: 1,
      ease: 'power2.out'
    }, 1.8 + index * 0.1)
  })
  
  // ===== 4. 植株弹性回弹（0.8-1.8s） =====
  timeline.to(stemGroup, {
    duration: 0.4,
    rotation: -6,
    transformOrigin: 'center bottom',
    ease: 'elastic.out(1, 0.5)'
  }, 0.8)
  
  timeline.to(stemGroup, {
    duration: 0.3,
    rotation: 3,
    transformOrigin: 'center bottom',
    ease: 'elastic.out(1, 0.6)'
  }, 1.2)
  
  timeline.to(stemGroup, {
    duration: 0.3,
    rotation: 0,
    transformOrigin: 'center bottom',
    ease: 'elastic.out(1, 0.7)'
  }, 1.5)
  
  // 叶子弹性回弹
  allLeaves.forEach((leaf, index) => {
    timeline.to(leaf, {
      duration: 0.35,
      rotation: -8,
      transformOrigin: 'left center',
      ease: 'elastic.out(1, 0.5)'
    }, 0.8 + index * 0.02)
    
    timeline.to(leaf, {
      duration: 0.3,
      rotation: 4,
      transformOrigin: 'left center',
      ease: 'elastic.out(1, 0.6)'
    }, 1.15 + index * 0.02)
    
    timeline.to(leaf, {
      duration: 0.35,
      rotation: 0,
      transformOrigin: 'left center',
      ease: 'elastic.out(1, 0.7)'
    }, 1.45 + index * 0.02)
  })
  
  // ===== 5. 显示祝福语（2.0s） =====
  timeline.call(() => {
    showBlessing.value = true
  }, [], 2.0)
  
  // ===== 6. 冷却时间 =====
  if (cooldownTimeout) clearTimeout(cooldownTimeout)
  cooldownTimeout = window.setTimeout(() => {
    // 2.5秒后才能再次触发
  }, 2500)
}

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
  if (cooldownTimeout) clearTimeout(cooldownTimeout)
})
</script>

<style scoped>
.magic-plant-container {
  position: fixed;
  bottom: 20px;
  left: 20px;
  z-index: 50;
  cursor: pointer;
}

.magic-plant {
  width: 130px;
  height: 180px;
  pointer-events: none;
  filter: drop-shadow(0 6px 16px rgba(0, 0, 0, 0.12));
  transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.magic-plant-container:hover .magic-plant {
  transform: translateY(-6px) scale(1.02);
}

.magic-plant-container:active .magic-plant {
  transform: translateY(-3px) scale(0.98);
}

.blessing-tooltip {
  position: absolute;
  bottom: 55%;
  left: 145px;
  transform: translateY(50%);
  background: rgba(255, 255, 255, 0.97);
  backdrop-filter: blur(14px);
  padding: 15px 24px;
  border-radius: 16px;
  border: 1.5px solid rgba(107, 142, 35, 0.3);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12), 0 3px 10px rgba(107, 142, 35, 0.15);
  font-size: 14px;
  color: #333;
  font-weight: 500;
  writing-mode: horizontal-tb;
  white-space: normal;
  word-break: break-word;
  min-width: 170px;
  max-width: 290px;
  line-height: 1.6;
}

.dark .blessing-tooltip {
  background: rgba(30, 41, 59, 0.97);
  color: #e2e8f0;
  border-color: rgba(107, 142, 35, 0.25);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3), 0 3px 10px rgba(107, 142, 35, 0.1);
}

.blessing-tooltip::before {
  content: '';
  position: absolute;
  top: 50%;
  right: 100%;
  transform: translateY(-50%);
  border: 10px solid transparent;
  border-right-color: rgba(255, 255, 255, 0.97);
  filter: drop-shadow(-3px 0 3px rgba(0, 0, 0, 0.08));
}

.dark .blessing-tooltip::before {
  border-right-color: rgba(30, 41, 59, 0.97);
}

.fade-enter-active {
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.fade-leave-active {
  transition: all 0.35s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(50%) translateX(-18px) scale(0.9);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(50%) translateX(-12px) scale(0.95);
}

@media (max-width: 768px) {
  .magic-plant-container {
    display: none;
  }
}
</style>
