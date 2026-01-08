import { test, expect } from '@playwright/test'

test.describe('Screenshots for README', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')
    await page.waitForTimeout(1000)
  })

  test('capture main interface', async ({ page }) => {
    // Take main interface screenshot
    await page.screenshot({
      path: '../docs/images/main-interface.png',
      fullPage: false
    })
  })

  test('capture natural language query workflow', async ({ page }) => {
    // Select database
    const dbItem = page.locator('text=pg__db_target').first()
    if (await dbItem.isVisible()) {
      await dbItem.click()
      await page.waitForTimeout(2000)
    }

    // Screenshot 1: Database selected with table structure
    await page.screenshot({
      path: '../docs/images/database-selected.png',
      fullPage: false
    })

    // Enter natural language query
    const queryInput = page.locator('input[placeholder*="自然语言"]')
    await queryInput.fill('查询所有设备信息，按设备类型分组统计数量')
    await page.waitForTimeout(500)

    // Screenshot 2: Natural language input
    await page.screenshot({
      path: '../docs/images/natural-query-input.png',
      fullPage: false
    })

    // Click generate SQL button
    const generateBtn = page.getByRole('button', { name: /生成 SQL/ })
    await generateBtn.click()

    // Wait for SQL generation
    await page.waitForTimeout(5000)

    // Screenshot 3: Generated SQL
    await page.screenshot({
      path: '../docs/images/generated-sql.png',
      fullPage: false
    })

    // Click apply to editor button if visible
    const applyBtn = page.getByRole('button', { name: /应用到编辑器/ })
    if (await applyBtn.isVisible()) {
      await applyBtn.click()
      await page.waitForTimeout(500)
    }

    // Execute query
    const executeBtn = page.getByRole('button', { name: /执行查询/ })
    await executeBtn.click()

    // Wait for results
    await page.waitForTimeout(3000)

    // Screenshot 4: Query results
    await page.screenshot({
      path: '../docs/images/query-results.png',
      fullPage: false
    })
  })

  test('capture another query example', async ({ page }) => {
    // Select database
    const dbItem = page.locator('text=pg__db_target').first()
    if (await dbItem.isVisible()) {
      await dbItem.click()
      await page.waitForTimeout(2000)
    }

    // Enter different natural language query
    const queryInput = page.locator('input[placeholder*="自然语言"]')
    await queryInput.fill('查询最近7天的轨迹数据，显示开始时间、结束时间和点数')
    await page.waitForTimeout(500)

    // Click generate SQL button
    const generateBtn = page.getByRole('button', { name: /生成 SQL/ })
    await generateBtn.click()

    // Wait for SQL generation
    await page.waitForTimeout(5000)

    // Apply and execute
    const applyBtn = page.getByRole('button', { name: /应用到编辑器/ })
    if (await applyBtn.isVisible()) {
      await applyBtn.click()
      await page.waitForTimeout(500)
    }

    const executeBtn = page.getByRole('button', { name: /执行查询/ })
    await executeBtn.click()

    // Wait for results
    await page.waitForTimeout(3000)

    // Screenshot: Another query example
    await page.screenshot({
      path: '../docs/images/query-example-2.png',
      fullPage: false
    })
  })
})
