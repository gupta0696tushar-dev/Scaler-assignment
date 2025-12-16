import { test, expect } from '@playwright/test'

test.describe('Visual Testing', () => {
  test.beforeEach(async ({ page }) => {
    // Wait for page to load
    await page.goto('/')
    await page.waitForLoadState('networkidle')
  })

  test('Home page layout', async ({ page }) => {
    // Mask dynamic content
    await page.addStyleTag({
      content: `
        [data-testid="dynamic-content"] {
          visibility: hidden;
        }
      `,
    })

    // Take screenshot
    await expect(page).toHaveScreenshot('home-page.png', {
      fullPage: true,
      mask: [page.locator('[data-testid="dynamic-content"]')],
    })
  })

  test('Projects page layout', async ({ page }) => {
    await page.goto('/projects')
    await page.waitForLoadState('networkidle')

    await expect(page).toHaveScreenshot('projects-page.png', {
      fullPage: true,
    })
  })

  test('Tasks page layout', async ({ page }) => {
    await page.goto('/tasks')
    await page.waitForLoadState('networkidle')

    await expect(page).toHaveScreenshot('tasks-page.png', {
      fullPage: true,
    })
  })

  test('CSS property assertions - Primary color', async ({ page }) => {
    await page.goto('/')
    
    // Check primary color on buttons/links
    const primaryElement = page.locator('text=Clooney').first()
    const color = await primaryElement.evaluate((el) => {
      return window.getComputedStyle(el).color
    })
    
    // Asana primary color: #3a258e (rgb(58, 37, 142))
    expect(color).toBe('rgb(58, 37, 142)')
  })
})

