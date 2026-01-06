# Fake Social Media Post Generator

A simple, client-side web application to generate fake social media posts (Telegram, iOS) for preview and export.

## Features

- **Mobile First Design**: Optimized for mobile viewing.
- **Multiple Themes**:
    - Telegram Dark
    - Telegram Light
    - iOS Message
- **Real-time Preview**: See changes instantly as you type.
- **Avatar Upload**: Supports local image preview.
- **High Quality Export**: Downloads the generated post as a high-resolution PNG using `html2canvas`.

## How to Use

1. **Clone or Download** the repository.
2. Open `index.html` in any modern web browser.
3. Fill in the details:
    - Choose a style (Theme).
    - Enter a Name, Message, and Time.
    - Upload an Avatar image.
4. Click **Download Image** to save the result.

## Tech Stack

- **HTML5**
- **CSS3** (Tailwind CSS via CDN)
- **JavaScript** (Vanilla)
- **Libraries**:
    - [html2canvas](https://html2canvas.hertzen.com/) (Screenshot generation)
    - [FontAwesome](https://fontawesome.com/) (Icons)

## License

MIT
