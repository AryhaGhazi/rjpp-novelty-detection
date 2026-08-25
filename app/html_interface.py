"""
Simple HTML interface for RJPP Novelty Detection
Access at: http://127.0.0.1:8000/interface
"""

HTML_INTERFACE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>RJPP Novelty Detection - Interface</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        header {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        
        .subtitle {
            color: #666;
            font-size: 14px;
        }
        
        .main-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
        
        .card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .card h2 {
            color: #667eea;
            margin-bottom: 20px;
            font-size: 20px;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .upload-area {
            border: 2px dashed #667eea;
            border-radius: 8px;
            padding: 40px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            background: #f8f9ff;
        }
        
        .upload-area:hover {
            background: #f0f2ff;
            border-color: #764ba2;
        }
        
        .upload-area input {
            display: none;
        }
        
        .upload-icon {
            font-size: 48px;
            margin-bottom: 15px;
        }
        
        input[type="file"],
        input[type="number"],
        select {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 14px;
        }
        
        button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 30px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            font-weight: bold;
            transition: all 0.3s ease;
            width: 100%;
            margin-top: 10px;
        }
        
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        .innovations-list {
            max-height: 400px;
            overflow-y: auto;
        }
        
        .innovation-item {
            background: #f8f9ff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }
        
        .innovation-title {
            font-weight: bold;
            color: #333;
            margin-bottom: 8px;
        }
        
        .score-badge {
            display: inline-block;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-right: 8px;
            margin-bottom: 8px;
        }
        
        .novelty-score {
            background: #e3f2fd;
            color: #1976d2;
        }
        
        .freshness-score {
            background: #f3e5f5;
            color: #7b1fa2;
        }
        
        .freshness-very-fresh {
            background: #c8e6c9;
            color: #2e7d32;
        }
        
        .freshness-fresh {
            background: #ffe0b2;
            color: #e65100;
        }
        
        .freshness-less-fresh {
            background: #ffccbc;
            color: #d84315;
        }
        
        .stats {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .stat-item {
            background: #f0f2ff;
            padding: 15px;
            border-radius: 5px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .alert {
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            display: none;
        }
        
        .alert.success {
            background: #c8e6c9;
            color: #2e7d32;
            border-left: 4px solid #2e7d32;
        }
        
        .alert.error {
            background: #ffcdd2;
            color: #c62828;
            border-left: 4px solid #c62828;
        }
        
        .alert.info {
            background: #bbdefb;
            color: #1565c0;
            border-left: 4px solid #1565c0;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            border-bottom: 1px solid #ddd;
        }
        
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            color: #666;
            border: none;
            background: none;
            font-size: 14px;
            font-weight: bold;
            border-bottom: 2px solid transparent;
            transition: all 0.3s ease;
        }
        
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        
        .comparison-table th,
        .comparison-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        .comparison-table th {
            background: #f0f2ff;
            color: #667eea;
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 RJPP Novelty Detection System</h1>
            <p class="subtitle">Sistem deteksi inovasi dokumen RJPP dengan penilaian freshness ide</p>
        </header>
        
        <div class="main-content">
            <!-- Upload Section -->
            <div class="card">
                <h2>📤 Upload RJPP Document</h2>
                
                <div class="upload-area" onclick="document.getElementById('fileInput').click()">
                    <div class="upload-icon">📄</div>
                    <p>Klik untuk upload atau drag & drop file PDF</p>
                    <input type="file" id="fileInput" accept=".pdf">
                </div>
                
                <input type="number" id="year" placeholder="Tahun RJPP (otomatis dari filename)" min="2000" max="2100">
                
                <button onclick="uploadFile()">Upload & Proses</button>
                
                <div id="uploadAlert" class="alert"></div>
                <div id="uploadLoading" class="loading">
                    <div class="spinner"></div>
                    <p>Memproses dokumen...</p>
                </div>
            </div>
            
            <!-- Stats Section -->
            <div class="card">
                <h2>📈 Statistik</h2>
                
                <div class="stats">
                    <div class="stat-item">
                        <div class="stat-value" id="totalInnovations">0</div>
                        <div class="stat-label">Total Inovasi</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="avgNovelty">0%</div>
                        <div class="stat-label">Avg Novelty</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="avgFreshness">0%</div>
                        <div class="stat-label">Avg Freshness</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value" id="yearsCount">0</div>
                        <div class="stat-label">Tahun Terdaftar</div>
                    </div>
                </div>
                
                <button onclick="refreshStats()">🔄 Refresh Statistik</button>
            </div>
        </div>
        
        <!-- Innovations Section -->
        <div class="card" style="margin-top: 20px;">
            <h2>🎯 Inovasi Terdeteksi</h2>
            
            <div class="tabs">
                <button class="tab active" onclick="switchTab('all-innovations')">Semua</button>
                <button class="tab" onclick="switchTab('by-year')">Per Tahun</button>
                <button class="tab" onclick="switchTab('comparison')">Perbandingan</button>
                <button class="tab" onclick="switchTab('documents')">Dokumen</button>
            </div>
            
            <!-- All Innovations Tab -->
            <div id="all-innovations" class="tab-content active">
                <div class="innovations-list" id="innovationsList">
                    <p style="color: #999; text-align: center;">Belum ada inovasi. Upload dokumen terlebih dahulu.</p>
                </div>
            </div>
            
            <!-- By Year Tab -->
            <div id="by-year" class="tab-content">
                <select id="yearFilter" onchange="filterByYear(this.value)" style="margin-bottom: 15px;">
                    <option value="">Pilih Tahun...</option>
                </select>
                <div class="innovations-list" id="innovationsByYear">
                    <p style="color: #999; text-align: center;">Pilih tahun untuk melihat inovasi.</p>
                </div>
            </div>
            
            <!-- Comparison Tab -->
            <div id="comparison" class="tab-content">
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Tahun</th>
                            <th>Jumlah Inovasi</th>
                            <th>Avg Novelty</th>
                            <th>Avg Freshness</th>
                        </tr>
                    </thead>
                    <tbody id="comparisonTable">
                        <tr>
                            <td colspan="4" style="text-align: center; color: #999;">
                                Belum ada data untuk perbandingan
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <!-- Documents Tab -->
            <div id="documents" class="tab-content">
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Filename</th>
                            <th>Tahun</th>
                            <th>Inovasi</th>
                            <th>Status</th>
                            <th>Tanggal Upload</th>
                        </tr>
                    </thead>
                    <tbody id="documentsTable">
                        <tr>
                            <td colspan="5" style="text-align: center; color: #999;">
                                Belum ada dokumen
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <script>
        const API_URL = 'http://127.0.0.1:8000/api';
        
        // File upload handling
        document.getElementById('fileInput').addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'Pilih file...';
            const uploadArea = document.querySelector('.upload-area p');
            if (e.target.files[0]) {
                uploadArea.textContent = `File dipilih: ${fileName}`;
            }
        });
        
        async function uploadFile() {
            const fileInput = document.getElementById('fileInput');
            const year = document.getElementById('year').value;
            const file = fileInput.files[0];
            
            if (!file) {
                showAlert('uploadAlert', 'Pilih file PDF terlebih dahulu', 'error');
                return;
            }
            
            const formData = new FormData();
            formData.append('file', file);
            if (year) formData.append('year', year);
            
            document.getElementById('uploadLoading').style.display = 'block';
            
            try {
                const response = await fetch(`${API_URL}/upload`, {
                    method: 'POST',
                    body: formData
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Upload gagal');
                }
                
                const data = await response.json();
                showAlert('uploadAlert', 
                    `✓ Berhasil upload! Terdeteksi ${data.innovations_detected} inovasi`, 
                    'success');
                
                fileInput.value = '';
                document.querySelector('.upload-area p').textContent = 'Klik untuk upload atau drag & drop file PDF';
                document.getElementById('year').value = '';
                
                await refreshAllData();
            } catch (error) {
                showAlert('uploadAlert', error.message, 'error');
            } finally {
                document.getElementById('uploadLoading').style.display = 'none';
            }
        }
        
        async function refreshAllData() {
            await refreshStats();
            await loadAllInnovations();
            await loadComparison();
            await loadDocuments();
            await loadYears();
        }
        
        async function refreshStats() {
            try {
                const response = await fetch(`${API_URL}/innovations`);
                const data = await response.json();
                
                const total = data.total;
                const avgNovelty = total > 0 ? 
                    (data.innovations.reduce((sum, i) => sum + i.novelty_score, 0) / total * 100).toFixed(1) : 0;
                const avgFreshness = total > 0 ?
                    (data.innovations.reduce((sum, i) => sum + i.freshness_score, 0) / total * 100).toFixed(1) : 0;
                
                document.getElementById('totalInnovations').textContent = total;
                document.getElementById('avgNovelty').textContent = avgNovelty + '%';
                document.getElementById('avgFreshness').textContent = avgFreshness + '%';
                
                const years = new Set(data.innovations.map(i => i.year));
                document.getElementById('yearsCount').textContent = years.size;
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        async function loadAllInnovations() {
            try {
                const response = await fetch(`${API_URL}/innovations`);
                const data = await response.json();
                
                const html = data.innovations.length > 0 ?
                    data.innovations.map(innovation => `
                        <div class="innovation-item">
                            <div class="innovation-title">${innovation.title}</div>
                            <div>
                                <span class="score-badge novelty-score">
                                    Novelty: ${(innovation.novelty_score * 100).toFixed(1)}%
                                </span>
                                <span class="score-badge freshness-${getFreshnessClass(innovation.freshness_score)}">
                                    ${innovation.freshness_category}
                                </span>
                            </div>
                            <small style="color: #666;">
                                Tahun ${innovation.year} | ${innovation.source_file}
                            </small>
                        </div>
                    `).join('') :
                    '<p style="color: #999; text-align: center;">Belum ada inovasi</p>';
                
                document.getElementById('innovationsList').innerHTML = html;
            } catch (error) {
                console.error('Error loading innovations:', error);
            }
        }
        
        async function loadYears() {
            try {
                const response = await fetch(`${API_URL}/innovations`);
                const data = await response.json();
                const years = [...new Set(data.innovations.map(i => i.year))].sort((a, b) => b - a);
                
                const select = document.getElementById('yearFilter');
                select.innerHTML = '<option value="">Pilih Tahun...</option>' +
                    years.map(year => `<option value="${year}">${year}</option>`).join('');
            } catch (error) {
                console.error('Error loading years:', error);
            }
        }
        
        async function filterByYear(year) {
            if (!year) {
                document.getElementById('innovationsByYear').innerHTML = 
                    '<p style="color: #999; text-align: center;">Pilih tahun untuk melihat inovasi.</p>';
                return;
            }
            
            try {
                const response = await fetch(`${API_URL}/innovations/year/${year}`);
                const data = await response.json();
                
                const html = data.innovations.length > 0 ?
                    data.innovations.map(innovation => `
                        <div class="innovation-item">
                            <div class="innovation-title">${innovation.title}</div>
                            <div>
                                <span class="score-badge novelty-score">
                                    Novelty: ${(innovation.novelty_score * 100).toFixed(1)}%
                                </span>
                                <span class="score-badge freshness-${getFreshnessClass(innovation.freshness_score)}">
                                    Freshness: ${(innovation.freshness_score * 100).toFixed(1)}%
                                </span>
                            </div>
                        </div>
                    `).join('') :
                    '<p style="color: #999; text-align: center;">Tidak ada inovasi untuk tahun ini</p>';
                
                document.getElementById('innovationsByYear').innerHTML = html;
            } catch (error) {
                console.error('Error filtering by year:', error);
            }
        }
        
        async function loadComparison() {
            try {
                const response = await fetch(`${API_URL}/comparison`);
                const data = await response.json();
                
                const html = data.years.length > 0 ?
                    data.years.map(year => {
                        const comp = data.comparison[year];
                        return `
                            <tr>
                                <td>${year}</td>
                                <td>${comp.count}</td>
                                <td>${(comp.avg_novelty * 100).toFixed(1)}%</td>
                                <td>${(comp.avg_freshness * 100).toFixed(1)}%</td>
                            </tr>
                        `;
                    }).join('') :
                    '<tr><td colspan="4" style="text-align: center; color: #999;">Belum ada data</td></tr>';
                
                document.getElementById('comparisonTable').innerHTML = html;
            } catch (error) {
                console.error('Error loading comparison:', error);
            }
        }
        
        async function loadDocuments() {
            try {
                const response = await fetch(`${API_URL}/documents`);
                const data = await response.json();
                
                const html = data.documents.length > 0 ?
                    data.documents.map(doc => `
                        <tr>
                            <td>${doc.filename}</td>
                            <td>${doc.year}</td>
                            <td>${doc.total_innovations}</td>
                            <td>${doc.processed === 1 ? '✓ Success' : doc.processed === 0 ? 'Pending' : '✗ Failed'}</td>
                            <td>${new Date(doc.created_at).toLocaleDateString('id-ID')}</td>
                        </tr>
                    `).join('') :
                    '<tr><td colspan="5" style="text-align: center; color: #999;">Belum ada dokumen</td></tr>';
                
                document.getElementById('documentsTable').innerHTML = html;
            } catch (error) {
                console.error('Error loading documents:', error);
            }
        }
        
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
        }
        
        function getFreshnessClass(score) {
            if (score >= 0.8) return 'very-fresh';
            if (score >= 0.6) return 'fresh';
            return 'less-fresh';
        }
        
        function showAlert(elementId, message, type) {
            const alert = document.getElementById(elementId);
            alert.className = `alert ${type}`;
            alert.textContent = message;
            alert.style.display = 'block';
            
            if (type === 'success') {
                setTimeout(() => {
                    alert.style.display = 'none';
                }, 3000);
            }
        }
        
        // Load data on page load
        window.addEventListener('load', refreshAllData);
    </script>
</body>
</html>
"""

def get_html_interface():
    return HTML_INTERFACE
