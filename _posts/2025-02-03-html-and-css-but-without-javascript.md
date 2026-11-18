---
title: "A two-step HTML and CSS form without JavaScript"
description: "Use the CSS :has() selector and a checked radio input to switch a rating form to a feedback field without JavaScript."
author: "sarbull"
tags: [html, css]
---

You can switch a two-step form from a rating to a feedback field using HTML radio inputs and the CSS `:has()` selector. When a radio input is checked, the selector matches its container, hides the rating, and reveals the textarea without JavaScript.

## HTML: rating and feedback fields

```html
<div class="container">
  <div class="rating">
    <input name="rating" type="radio" /> 1
    <input name="rating" type="radio" /> 2
    <input name="rating" type="radio" /> 3
    <input name="rating" type="radio" /> 4
    <input name="rating" type="radio" /> 5
  </div>
  
  <textarea name="feedback"></textarea>
</div>
```

## CSS: respond to a checked rating

```css
.container textarea { display:none; }
.container:has(.rating > input:checked) .rating { display:none; }
.container:has(.rating > input:checked) textarea { display:block; }
```

## Demo

![A rating selection revealing a feedback textarea without JavaScript]({{ "/demo-html-css-form.gif" | relative_url }}){: width="800" height="417" loading="lazy" decoding="async" }

See the [MDN documentation for :has()](https://developer.mozilla.org/en-US/docs/Web/CSS/:has) for selector behavior and browser compatibility. This example demonstrates the visibility change; add labels and a way to revise the rating when adapting it to a complete form.

For base styling, see [my CSS reset]({% post_url 2025-02-12-a-simple-reset-css %}).

