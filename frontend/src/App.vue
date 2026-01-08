<template>
  <el-config-provider :locale="zhCn">
    <div class="app-container min-h-screen bg-gray-50">
      <!-- Global Error Alert -->
      <div v-if="globalError" class="fixed top-0 left-0 right-0 z-50 p-4 bg-red-100 border-b border-red-300">
        <div class="max-w-4xl mx-auto flex items-center justify-between">
          <div class="flex items-center gap-2 text-red-700">
            <el-icon><WarningFilled /></el-icon>
            <span>{{ globalError }}</span>
          </div>
          <el-button size="small" type="danger" link @click="clearGlobalError">
            关闭
          </el-button>
        </div>
      </div>

      <el-container class="h-screen">
        <el-header class="bg-white border-b border-gray-200 flex items-center justify-between px-4 md:px-6">
          <h1 class="text-lg md:text-xl font-semibold text-gray-800 truncate">数据库查询工具</h1>
          <span class="text-xs text-gray-400 hidden sm:inline">v1.0.0</span>
        </el-header>
        <el-main class="p-0">
          <HomePage />
        </el-main>
      </el-container>
    </div>
  </el-config-provider>
</template>

<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue'
import { ElConfigProvider, ElContainer, ElHeader, ElMain, ElButton, ElIcon } from 'element-plus'
import { WarningFilled } from '@element-plus/icons-vue'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import HomePage from '@/pages/HomePage.vue'

const globalError = ref<string | null>(null)

// Global error boundary
onErrorCaptured((err) => {
  console.error('Application error:', err)
  globalError.value = err instanceof Error ? err.message : '应用发生错误'
  return false // Prevent error propagation
})

function clearGlobalError(): void {
  globalError.value = null
}
</script>

<style>
.app-container {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    sans-serif;
}

/* Fix nested el-container layout */
.home-page .el-container {
  display: flex;
  flex-direction: row;
  width: 100%;
}

.home-page .el-container > .el-main {
  flex: 1;
  min-width: 0; /* Prevent flex item from overflowing */
  overflow: auto;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .el-aside {
    width: 100% !important;
    border-right: none !important;
    border-bottom: 1px solid #e5e7eb;
    max-height: 40vh;
  }

  .el-container.h-full {
    flex-direction: column;
  }
}
</style>
