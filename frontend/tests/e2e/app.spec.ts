import { test, expect } from '@playwright/test'

test.describe('Database Query Tool', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    // Wait for the app to fully load
    await page.waitForLoadState('networkidle')
  })

  test('should display the main page with title', async ({ page }) => {
    // Check page title
    await expect(page.locator('h1')).toContainText('数据库查询工具')
  })

  test('should show database connection section', async ({ page }) => {
    // Check database connection header - use more specific selector
    await expect(page.getByRole('heading', { name: /数据库连接/ })).toBeVisible()

    // Check add button
    await expect(page.getByRole('button', { name: /添加/ })).toBeVisible()
  })

  test('should show empty database list message', async ({ page }) => {
    // Should show empty state when no databases - check if element exists
    const emptyText = page.getByText('暂无数据库连接')
    await expect(emptyText).toBeVisible({ timeout: 10000 })
  })

  test('should open add database dialog', async ({ page }) => {
    // Click add button
    await page.getByRole('button', { name: /添加/ }).click()

    // Dialog should appear
    await expect(page.locator('.el-dialog')).toBeVisible({ timeout: 10000 })
    await expect(page.getByText('添加数据库连接')).toBeVisible()
  })

  test('should show SQL query section', async ({ page }) => {
    // Check SQL query header
    await expect(page.getByRole('heading', { name: /SQL 查询/ })).toBeVisible()

    // Check execute button (should be visible but disabled when no database selected)
    const executeButton = page.getByRole('button', { name: /执行查询/ })
    await expect(executeButton).toBeVisible()
  })

  test('should show natural language query section', async ({ page }) => {
    // Check natural language query header
    await expect(page.getByRole('heading', { name: /自然语言查询/ })).toBeVisible()

    // Check generate SQL button
    const generateButton = page.getByRole('button', { name: /生成 SQL/ })
    await expect(generateButton).toBeVisible()
  })

  test('should show query result section', async ({ page }) => {
    // Check query result header
    await expect(page.getByRole('heading', { name: /查询结果/ })).toBeVisible()

    // Check placeholder text
    await expect(page.getByText('执行查询后显示结果')).toBeVisible()
  })

  test('add database dialog validation', async ({ page }) => {
    // Open dialog
    await page.getByRole('button', { name: /添加/ }).click()
    await expect(page.locator('.el-dialog')).toBeVisible({ timeout: 10000 })

    // Fill in the form - name input and URL textarea
    await page.locator('input[placeholder*="连接名称"]').fill('test-db')
    await page.locator('textarea[placeholder*="postgres"]').fill('postgresql://localhost/test')

    // Cancel dialog
    await page.getByRole('button', { name: /取消/ }).click()
    await expect(page.locator('.el-dialog')).not.toBeVisible()
  })
})
