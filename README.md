# 📊 Student Performance Analytics

Aplikasi web modern berbasis Streamlit untuk analisis, tracking, dan visualisasi performa siswa menggunakan PostgreSQL dengan antarmuka yang menarik dan interaktif.

## 📋 Struktur Folder

```
Tubes_Bismillah/
├── app.py                 # Main application
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── .gitignore            # Git ignore file
├── README.md             # Documentation
├── config/
│   └── settings.py       # Application settings
├── modules/
│   ├── database.py       # Database connection handler
│   └── utils.py          # Utility functions
├── pages/                # Multi-page app features
├── .streamlit/
│   └── config.toml       # Streamlit configuration
└── data/                 # Data folder
```

## 🚀 Quick Start

### 1. Setup Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` dan sesuaikan:

```bash
cp .env.example .env
```

Edit `.env` dengan konfigurasi database Anda:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=student_performance_db
DB_USER=postgres
DB_PASSWORD=your_password
```

### 4. Run Application

```bash
streamlit run app.py
```

Aplikasi akan berjalan di `http://localhost:8501`

## 📊 Database Schema

Aplikasi menggunakan 8 tabel utama:

1. **student** - Data siswa
2. **study_habits** - Kebiasaan belajar (1:1)
3. **exam_scores** - Nilai ujian (1:1)
4. **parent_background** - Latar belakang orang tua (1:N)
5. **services** - Layanan sekolah
6. **student_services** - Layanan siswa (M:N)
7. **activities** - Aktivitas ekstrakurikuler
8. **student_activities** - Aktivitas siswa (M:N)

## 🎨 Modern UI Features

- 🎨 **Beautiful Gradients** - Modern color schemes
- 📊 **Interactive Charts** - Plotly & Altair visualizations
- 🎯 **Responsive Design** - Works on all devices
- 🚀 **Fast Performance** - Optimized queries
- 🔄 **Real-time Updates** - Live data connection
- 📱 **Mobile Friendly** - Full responsive support

## 📈 Visualizations Included

1. **Bar Charts** - Grade distribution, service enrollment, activity participation
2. **Pie/Donut Charts** - Gender distribution, grade percentages, preferences
3. **Histograms** - Score distributions, study hours
4. **Box Plots** - Score ranges, outlier detection
5. **Violin Plots** - Distribution shapes, gender comparisons
6. **Scatter Plots** - Correlations, performance vs study hours
7. **Radar Charts** - Multi-dimensional score visualization
8. **Line Charts** - Trends and patterns
9. **Heatmaps** - Correlation matrices (coming soon)
10. **Sunburst Charts** - Hierarchical data (coming soon)

## ✨ Features

### 🏠 **Home Dashboard**

- Overview metrics (total students, average scores)
- Grade level distribution charts
- Exam scores histogram
- Gender and ethnicity distribution
- Real-time statistics

### 👥 **Student Management**

- View all students in data table
- Search students by name
- Detailed student information
- Personal data management

### 📊 **Analytics & Reports**

- **Study Habits Analysis**
  - Study hours distribution
  - Study preference (group vs solo)
  - Private tutor impact
- **Performance Analysis**
  - Score comparison charts
  - Radar visualization
  - Scatter plots
- **Services Analytics**
  - Service enrollment statistics
  - Usage metrics
- **Activities Analytics**
  - Participation statistics
  - Hours per week analysis

### 📈 **Performance Dashboard**

- Performance category distribution
- Top 10 performers ranking
- Study hours vs performance correlation
- Tutor impact visualization
- Grade level performance analysis
- Detailed performance table

### 👤 **Student Details (Pages)**

- Individual student profile
- Complete academic records
- Study habits breakdown
- Exam scores radar chart
- Parent background information
- Enrolled services
- Extracurricular activities

### 📊 **Comparison Analysis (Pages)**

- Grade level performance comparison
- Gender-based performance analysis
- Tutor impact assessment
- Statistical distributions
- Box plots and violin plots

### 💡 **Insights & Recommendations (Pages)**

- Key insights from data
- At-risk student identification
- Top performer showcase
- Data-driven recommendations
- Study habits impact analysis

### ⚙️ **Settings**

- Database configuration display
- Application status
- System information

## 🐛 Troubleshooting

### Database Connection Failed

1. Pastikan PostgreSQL sudah running
2. Cek `.env` file - DB credentials harus benar
3. Pastikan database `student_performance_db` sudah dibuat

### Port Already in Use

```bash
streamlit run app.py --server.port 8502
```

## 📚 Dokumentasi Lengkap

Untuk dokumentasi lengkap tentang setup dan development, lihat:

- [Streamlit Documentation](https://docs.streamlit.io)
- [PostgreSQL Documentation](https://www.postgresql.org/docs)

## 👨‍💻 Development

Untuk development, install dev dependencies tambahan:

```bash
pip install pytest pytest-cov black flake8
```

## 📄 License

Project ini adalah bagian dari tugas kuliah Administrasi Basis Data.
