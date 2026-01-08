<template>
  <div class="database-list">
    <div v-if="databases.length === 0" class="text-gray-400 text-sm">
      暂无数据库连接
    </div>
    <el-menu
      v-else
      :default-active="activeDb"
      class="border-none"
      @select="handleSelect"
    >
      <el-menu-item
        v-for="db in databases"
        :key="db.name"
        :index="db.name"
        class="flex items-center justify-between"
      >
        <div class="flex items-center gap-2">
          <el-icon>
            <component :is="db.dbType === 'postgres' ? 'Grape' : 'Coin'" />
          </el-icon>
          <span>{{ db.name }}</span>
        </div>
        <el-tag size="small" :type="db.dbType === 'postgres' ? 'primary' : 'success'">
          {{ db.dbType === 'postgres' ? 'PG' : 'MySQL' }}
        </el-tag>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { ElMenu, ElMenuItem, ElIcon, ElTag } from 'element-plus'
import { Grape, Coin } from '@element-plus/icons-vue'
import { useDatabaseStore } from '@/stores/database'

const store = useDatabaseStore()

const databases = computed(() => store.databases)
const activeDb = computed(() => store.currentDatabase?.name ?? '')

const emit = defineEmits<{
  select: [name: string]
}>()

function handleSelect(name: string): void {
  emit('select', name)
}
</script>

<style scoped>
.database-list :deep(.el-menu-item) {
  height: 40px;
  line-height: 40px;
}
</style>
