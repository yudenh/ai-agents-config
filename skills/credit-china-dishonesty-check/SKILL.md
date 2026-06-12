---
name: credit-china-dishonesty-check
description: "Use when: open headful browser pages for 信用中国失信查询, including 失信被执行人查询, 重大税收违法失信主体查询, and 政府采购严重违法失信行为记录名单查询."
---

# credit-china-dishonesty-check

Open the required public query pages in a headful browser and prefill known company information so the user can manually complete the searches.

## Use When

The user wants to query a company or organization in these public credit/discredit lists:

- `失信被执行人查询`
- `重大税收违法失信主体查询`
- `政府采购严重违法失信行为记录名单`

## Required Inputs

- `单位名称`
- `统一社会信用代码` or `组织机构代码`

If either value is missing, ask the user for it before opening the pages.

## Browser Requirement

- Special emphasis: the browser MUST be opened in headed/headful mode.
- Never use headless mode for this skill.
- The user must manually participate in verification, captcha, and final query submission, so a visible browser window is required.
- `playwright-cli` is the tool reference for how to launch the browser.
- Leave all opened pages visible for the user.

## Steps

1. Execute `playwright-cli open https://zxgk.court.gov.cn/shixin/ --headed`.
2. Maximize the browser window.
3. Fill `单位名称` into the `被执行人姓名/名称` input.
4. Fill `统一社会信用代码` or `组织机构代码` into the `身份证号码/组织机构代码` input.
5. Open `https://www.creditchina.gov.cn/zhuanxiangchaxun/zhongdashuishouweifaanjian/`.
6. Fill `单位名称` into the input immediately to the left of the `查 询` button.
7. Open `https://www.creditchina.gov.cn/zhuanxiangchaxun/zhengfucaigouyanzhongweifashixinmingdan/`.
8. Fill `单位名称` into the input immediately to the left of the `查 询` button.
9. Tell the user that all pages have been opened and prefilled, and that they should manually complete each query.

## Notes

- Do not click the final query buttons unless the user explicitly asks for it.
- If a page shows a captcha, slider, pop-up, or browser security prompt, stop automation on that page and ask the user to handle it manually.
- If a selector is unstable, locate fields by nearby visible labels or by the `查 询` button relationship rather than relying only on CSS selectors.
