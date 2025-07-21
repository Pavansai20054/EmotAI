# 🎭 EmotAI - AI-Powered Emoji Suggestion System

<div align="center">

![EmotAI Logo](https://img.shields.io/badge/EmotAI-🎭%20AI%20Powered-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![React](https://img.shields.io/badge/React-18.2.0-61DAFB?style=for-the-badge&logo=react)
![Flask](https://img.shields.io/badge/Flask-Backend-000000?style=for-the-badge&logo=flask)

**Making every message mean more!** 💬❤️

</div>

---

## 🌟 What is EmotAI?

EmotAI is an **intelligent emoji suggestion system** that uses advanced AI and Natural Language Processing to analyze your text messages and suggest the most appropriate emojis based on sentiment, context, and emotion. It bridges the emotional gap in digital communication by making text-based conversations more expressive and emotionally rich! 🚀

### ✨ Key Features

- 🧠 **Advanced AI Integration**: Powered by Google's Gemini API for intelligent emoji suggestions
- 🎯 **Smart Sentiment Analysis**: Detects emotions like happiness, sadness, love, excitement, and more
- 📊 **Real-time Analytics**: Track emoji usage patterns and user preferences
- 🔄 **Fallback System**: Ensures suggestions even when AI services are unavailable
- 🌐 **Web Interface**: Beautiful React-based frontend with smooth animations
- 📱 **API Ready**: RESTful API for easy integration with other applications
- 🔗 **Webhook Support**: Integration with Slack, Teams, and other platforms
- 📈 **User Feedback**: Continuous improvement through user ratings and feedback

---

## 🏗️ Project Architecture

```
EmotAI/
├── 🖥️ Frontend (React)
│   ├── Modern UI with animations
│   ├── Real-time emoji suggestions
│   └── Interactive feedback system
│
├── ⚙️ Backend (Flask)
│   ├── AI-powered sentiment analysis
│   ├── RESTful API endpoints
│   ├── Database management
│   └── Analytics & feedback processing
│
├── 🤖 AI Engine
│   ├── Google Gemini API integration
│   ├── TextBlob sentiment analysis
│   ├── Custom emoji mapping
│   └── Intelligent fallback system
│
└── 🗄️ Database (SQLite)
    ├── User management
    ├── Message history
    ├── Feedback storage
    └── Analytics data
```

---

## 🚀 Quick Start Guide

### 📋 Prerequisites

Before you begin, make sure you have:

- 🐍 **Python 3.8+** installed
- 📦 **Node.js 14+** and npm
- 🔑 **Google Gemini API Key** ([Get it here](https://makersuite.google.com/app/apikey))

### 🛠️ Installation Steps

#### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Pavansai20054/EmotAI.git
cd EmotAI
```

#### 2️⃣ Backend Setup

```bash
# Navigate to backend directory
cd Code/backend

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

#### 3️⃣ Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install
```

#### 4️⃣ Environment Configuration

Create a `.env` file in the `Code` directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
```

#### 5️⃣ Run the Application

**Start Backend Server:**

```bash
cd Code/backend
python app.py
```

🌐 Backend will run on: `http://localhost:5000`

**Start Frontend Server:**

```bash
cd Code/frontend
npm start
```

🌐 Frontend will run on: `http://localhost:3000`

### 🎉 You're All Set!

Open your browser and navigate to `http://localhost:3000` to start using EmotAI!

---

## 🎯 How It Works

### 1️⃣ **Message Input**

User types a message in the web interface or sends it via API

### 2️⃣ **Sentiment Analysis**

- TextBlob analyzes the emotional tone
- Custom algorithms detect context and intensity
- Multiple emotion categories are identified

### 3️⃣ **AI Processing**

- Google Gemini API generates contextual emoji suggestions
- Advanced prompting ensures relevant results
- Fallback system activates if needed

### 4️⃣ **Smart Suggestions**

- Up to 15 relevant emojis are suggested
- Emojis are categorized by intensity (mild, moderate, strong)
- Explanations provided for better understanding

### 5️⃣ **User Feedback**

- Users can rate suggestions (1-3 stars)
- Feedback improves future recommendations
- Analytics track usage patterns

---

## 🔧 API Endpoints

### 📝 Emoji Suggestions

```http
POST /suggest
Content-Type: application/json

{
  "message": "I'm so happy today!"
}
```

**Response:**

```json
{
  "emojis": ["😊", "😄", "🎉", "✨", "🌟"],
  "message": "I'm so happy today!",
  "explanation": "Detected positive sentiment with high happiness intensity"
}
```

### 📊 Analytics

```http
GET /analytics
```

### 💬 Feedback

```http
POST /feedback
Content-Type: application/json

{
  "message_id": 123,
  "rating": 3,
  "comment": "Great suggestions!"
}
```

### 🔗 Webhook Integration

```http
POST /integrations/webhook
```

---

## 🎨 Technology Stack

### Frontend 🖥️

- **React 18.2.0** - Modern UI framework
- **Framer Motion** - Smooth animations
- **React Spring** - Interactive transitions
- **Styled Components** - Dynamic styling

### Backend ⚙️

- **Flask** - Lightweight web framework
- **SQLAlchemy** - Database ORM
- **Flask-CORS** - Cross-origin support
- **Pydantic** - Data validation

### AI & ML 🤖

- **Google Gemini API** - Advanced text generation
- **TextBlob** - Sentiment analysis
- **Custom NLP** - Emotion detection
- **Transformers** - Advanced language processing

### Database 🗄️

- **SQLite** - Development database
- **PostgreSQL** - Production ready (optional)

---

## 📈 Features in Detail

### 🧠 Advanced Sentiment Analysis

- **Multi-emotion Detection**: Happy, sad, love, excited, angry, danger, and more
- **Intensity Levels**: Mild, moderate, and strong emotional expressions
- **Context Awareness**: Understanding sarcasm, mixed emotions, and cultural nuances
- **Language Support**: Multi-language sentiment detection

### 🎭 Intelligent Emoji Mapping

- **Contextual Suggestions**: Emojis that match the exact emotional tone
- **Cultural Sensitivity**: Appropriate emojis for different contexts
- **Personalization**: Learning from user preferences over time
- **Fallback System**: Always provides suggestions, even offline

### 📊 Analytics Dashboard

- **Usage Statistics**: Track most popular emojis and sentiments
- **User Insights**: Understand communication patterns
- **Performance Metrics**: API response times and accuracy rates
- **Feedback Analysis**: Continuous improvement insights

### 🔗 Integration Capabilities

- **Webhook Support**: Easy integration with chat platforms
- **REST API**: Simple integration with any application
- **SDK Ready**: Future mobile and desktop app support
- **Plugin Architecture**: Extensible for custom integrations

---

## 🐳 Docker Deployment

### Quick Docker Setup

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or run individual containers
docker build -t emojai-backend ./Code/backend
docker build -t emojai-frontend ./Code/frontend

docker run -p 5000:5000 emojai-backend
docker run -p 3000:3000 emojai-frontend
```

---

## 🧪 Testing

### Run Backend Tests

```bash
cd Code
pytest tests/ -v
```

### Test Coverage

- ✅ Sentiment analysis accuracy
- ✅ API endpoint functionality
- ✅ Database operations
- ✅ Error handling and fallbacks

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 **Fork the repository**
2. 🌿 **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. 💻 **Make your changes**
4. ✅ **Add tests** for new functionality
5. 📝 **Commit your changes**: `git commit -m 'Add amazing feature'`
6. 🚀 **Push to branch**: `git push origin feature/amazing-feature`
7. 🔄 **Open a Pull Request**

### 📋 Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint for JavaScript code
- Write comprehensive tests
- Update documentation for new features

---

## 🛠️ Troubleshooting

### Common Issues & Solutions

#### 🔑 API Key Issues

```bash
# Ensure your .env file has the correct API key
GEMINI_API_KEY=your_actual_api_key_here
```

#### 📦 Dependency Issues

```bash
# Update pip and reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

#### 🌐 CORS Issues

```bash
# Ensure Flask-CORS is properly configured
pip install flask-cors
```

#### 🗄️ Database Issues

```bash
# Reset database if needed
rm backend/instance/emotiai.db
python backend/app.py  # This will recreate the database
```

---

## 📚 Documentation

- 📖 **[API Documentation](./Documentation/)** - Detailed API reference
- 🎯 **[User Guide](./Documentation/)** - How to use EmotAI effectively
- 🔧 **[Developer Guide](./Documentation/)** - Technical implementation details
- 📊 **[Analytics Guide](./Documentation/)** - Understanding usage analytics

---

## 🌍 Roadmap

### 🔮 Upcoming Features

- 📱 **Mobile App**: Native iOS and Android applications
- 🌐 **Multi-language Support**: Support for 20+ languages
- 🎨 **Custom Emoji Sets**: User-defined emoji collections
- 🤖 **Advanced AI**: GPT-4 integration for better context understanding
- 📈 **Enterprise Features**: Team analytics and admin controls
- 🔌 **More Integrations**: WhatsApp, Telegram, Discord support

### 🎯 Version History

- **v1.0.0** - Initial release with basic emoji suggestions
- **v1.1.0** - Added analytics and feedback system
- **v1.2.0** - Improved AI accuracy and web interface
- **v2.0.0** - Complete rewrite with advanced features (Current)

---

## 👥 Meet Our Team

<div align="center">

### 🎓 **KG Reddy College of Engineering & Technology**

### 📅 **Academic Year: 2024-25**

</div>

| 👨‍💻 **Team Member**   | 🎯 **Role**                    | 📧 **Contact**                                            |
| -------------------- | ------------------------------ | --------------------------------------------------------- |
| **Rangdal Pavansai** | 🚀 Project Lead & AI Developer | [LinkedIn](https://www.linkedin.com/in/rangdal-pavansai/) |
| **Wagmare Sanjana**  | 🎨 Frontend Developer & UI/UX  | [LinkedIn](https://www.linkedin.com/in/wagmare-sanjana)   |
| **U Sai Hruthvin**   | ⚙️ Researcher                  | -                                                         |

---

## 📞 Contact & Support

### 📧 **Get in Touch**

- **Primary Contact**: psai49779@gmail.com
- **Support Email**: wagmaresanjana5@gmail.com
- **LinkedIn**: [Rangdal Pavansai](https://www.linkedin.com/in/rangdal-pavansai/)

### 🐛 **Report Issues**

Found a bug? Have a feature request?

- 🔗 [Open an Issue](https://github.com/your-repo/issues)
- 💬 [Join our Discord](https://discord.gg/your-server)
- 📧 Email us directly

### 💡 **Feature Requests**

We love hearing your ideas! Share your suggestions:

- 🌟 [Feature Request Form](https://github.com/your-repo/issues/new?template=feature_request.md)
- 💭 [Community Discussions](https://github.com/your-repo/discussions)

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 EmotAI Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🙏 Acknowledgments

- 🤖 **Google Gemini API** - For powerful AI text generation
- 🐍 **Python Community** - For amazing libraries and tools
- ⚛️ **React Community** - For the fantastic frontend framework
- 🎨 **Open Source Community** - For inspiration and contributions
- 🎓 **KG Reddy College** - For academic support and guidance

---

## 🌟 Show Your Support

If you find EmotAI helpful, please consider:

- ⭐ **Star this repository**
- 🍴 **Fork and contribute**
- 📢 **Share with friends**
- 💬 **Leave feedback**

---

<div align="center">

### 🎭 **EmotAI: Making every message mean more!** 💬❤️

**Built with ❤️ by the EmotAI Team**

[![Made with Love](https://img.shields.io/badge/Made%20with-❤️-red?style=for-the-badge)](https://github.com/your-repo)
[![Python](https://img.shields.io/badge/Made%20with-Python-blue?style=for-the-badge&logo=python)](https://python.org)
[![React](https://img.shields.io/badge/Made%20with-React-61DAFB?style=for-the-badge&logo=react)](https://reactjs.org)

</div>

---

_Last updated: January 2025_ 📅
