# mapova_ai_compact.py
import http.server, socketserver, json, urllib.parse, requests

GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

HTML_CONTENT = r"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MAPOVA AI</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/12.6.0/firebase-app.js";
        import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword, signOut, onAuthStateChanged, sendEmailVerification, sendPasswordResetEmail } from "https://www.gstatic.com/firebasejs/12.6.0/firebase-auth.js";

        const firebaseConfig = {
            apiKey: "AIzaSyCX59Tn0caqhbIqUiTZcKuUV8gcwj_HNdM",
            authDomain: "mapova-ai.firebaseapp.com",
            projectId: "mapova-ai",
            storageBucket: "mapova-ai.firebasestorage.app",
            messagingSenderId: "449751655584",
            appId: "1:449751655584:web:6e586fc7e3dbf06f4c15c5",
            measurementId: "G-482ECV4WQ9"
        };

        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);

        window.firebaseAuth = {
            auth: auth,
            createUserWithEmailAndPassword: createUserWithEmailAndPassword,
            signInWithEmailAndPassword: signInWithEmailAndPassword,
            signOut: signOut,
            onAuthStateChanged: onAuthStateChanged,
            sendEmailVerification: sendEmailVerification,
            sendPasswordResetEmail: sendPasswordResetEmail
        };
    </script>
    <style>
    h3{
    text-align:center;
    }
        *{margin:0;padding:0;box-sizing:border-box;}
        body{font-family:Arial,sans-serif;background:#111;color:#fff;height:100vh;display:flex;flex-direction:column;}
        
        #menu-toggle{display:none;}
        .menu-section{position:fixed;top:15px;left:15px;z-index:1000;}
        .menu-btn{display:flex;flex-direction:column;cursor:pointer;padding:10px;}
        .menu-btn span{width:25px;height:3px;background:#00FF88;margin:3px 0;transition:0.3s;}
        #menu-toggle:checked ~ .menu-section .menu-btn span:nth-child(1){transform:rotate(-45deg) translate(-5px,6px);}
        #menu-toggle:checked ~ .menu-section .menu-btn span:nth-child(2){opacity:0;}
        #menu-toggle:checked ~ .menu-section .menu-btn span:nth-child(3){transform:rotate(45deg) translate(-5px,-6px);}
        .nav-menu{position:fixed;top:60px;left:-300px;width:250px;height:100vh;background:#1a1a1a;transition:0.3s;padding:20px;border-right:1px solid #333;overflow-y:auto;}
        #menu-toggle:checked ~ .menu-section .nav-menu{left:0;}
        .nav-menu a{display:block;color:#fff;text-decoration:none;padding:12px;margin:5px 0;border-radius:5px;transition:0.3s;}
        .nav-menu a:hover{background:#00FF88;color:#000;}
        .nav-menu a i{margin-right:10px;width:20px;}
        
        .content-section{display:none;padding:20px;max-width:800px;margin:0 auto;width:100%;}
        .content-section.active{display:block;}
        .content-section h2{color:#00FF88;margin-bottom:15px;border-bottom:2px solid #00FF88;padding-bottom:5px;}
        
        .auth-form{max-width:400px;margin:20px auto;background:#2a2a2a;padding:30px;border-radius:10px;border:1px solid #444;}
        .form-group{margin-bottom:20px;}
        .form-group label{display:block;margin-bottom:5px;color:#00FF88;font-weight:bold;}
        .form-group input{width:100%;padding:12px;border:none;border-radius:5px;background:#1a1a1a;color:white;font-size:16px;outline:none;border:1px solid #444;}
        .form-group input:focus{border-color:#00FF88;}
        .auth-btn{width:100%;padding:12px;background:#00FF88;color:#000;border:none;border-radius:5px;cursor:pointer;font-weight:bold;font-size:16px;}
        .auth-switch{text-align:center;margin-top:20px;color:#ccc;}
        .auth-switch a{color:#00FF88;text-decoration:none;}
        .forgot-password{text-align:center;margin-top:15px;}
        .forgot-password a{color:#00a8ff;text-decoration:none;font-size:14px;}
        .error-message{color:#ff4757;text-align:center;margin-top:10px;padding:10px;background:rgba(255,71,87,0.1);border-radius:5px;}
        .success-message{color:#00FF88;text-align:center;margin-top:10px;padding:10px;background:rgba(0,255,136,0.1);border-radius:5px;}
        
        .header{background:#1a1a1a;padding:15px 20px;border-bottom:1px solid #333;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;}
        .logo{font-size:20px;font-weight:bold;color:#00FF88;}
        .status{font-size:12px;color:#00FF88;background:rgba(0,255,136,0.1);padding:4px 8px;border-radius:10px;}
        .user-info{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:flex-end;flex:1;min-width:0;}
        .user-email{color:#00FF88;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:120px;}
        .logout-btn{padding:6px 12px;background:#ff4757;color:white;border:none;border-radius:5px;cursor:pointer;font-size:12px;white-space:nowrap;}
        
        .profile-info{background:#2a2a2a;padding:20px;border-radius:10px;border:1px solid #444;margin-bottom:20px;}
        .profile-details h3{color:#00FF88;margin-bottom:10px;text-align:left;}
        .profile-stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin-top:15px;}
        .stat-card{background:#1a1a1a;padding:12px;border-radius:8px;text-align:center;border:1px solid #444;}
        .stat-number{color:#00FF88;font-size:20px;font-weight:bold;}
        .stat-label{color:#ccc;font-size:11px;}
        
        .chat-container{flex:1;display:flex;flex-direction:column;max-width:800px;margin:0 auto;width:100%;padding:20px;}
        .chat-messages{flex:1;overflow-y:auto;padding:20px;margin-bottom:20px;background:#1a1a1a;border-radius:10px;border:1px solid #333;}
        .message{padding:15px 20px;margin:15px 0;border-radius:15px;max-width:80%;word-wrap:break-word;line-height:1.5;}
        .user-message{background:#00FF88;color:#000;margin-left:auto;border-bottom-right-radius:5px;}
        .ai-message{background:#2a2a2a;border:1px solid #444;margin-right:auto;border-bottom-left-radius:5px;}
        .chat-input-container{display:flex;gap:10px;padding:15px;background:#1a1a1a;border-radius:10px;border:1px solid #333;}
        #chat-input{flex:1;padding:12px 15px;border:none;border-radius:25px;background:#2a2a2a;color:white;font-size:16px;outline:none;}
        #send-btn{padding:12px 25px;background:#00FF88;color:#000;border:none;border-radius:25px;cursor:pointer;font-weight:bold;}
        .typing-indicator{display:none;padding:15px 20px;margin:15px 0;background:#2a2a2a;border:1px solid #444;border-radius:15px;max-width:80%;}
        .typing-dots{display:flex;gap:4px;}
        .typing-dots span{width:8px;height:8px;background:#00FF88;border-radius:50%;animation:typing 1.4s infinite;}
        @keyframes typing{0%,60%,100%{transform:translateY(0);opacity:0.4;}30%{transform:translateY(-5px);opacity:1;}}
        
        @media (max-width:768px){
            .message{max-width:95%;}
            .chat-container{padding:10px;}
            .header{padding:12px 15px;gap:8px;}
            .user-info{justify-content:center;margin-top:5px;}
            .user-email{max-width:100px;font-size:12px;}
            .profile-stats{grid-template-columns:repeat(2,1fr);}
        }
        @media (max-width:480px){
            .header{flex-direction:column;text-align:center;}
            .user-info{justify-content:center;width:100%;}
            .user-email{max-width:180px;}
        }
    </style>
</head>
<body>
    <input type="checkbox" id="menu-toggle">
    <div class="menu-section">
        <label class="menu-btn" for="menu-toggle"><span></span><span></span><span></span></label>
        <nav class="nav-menu" id="nav-menu">
            <a href="#" data-section="home"><i class="fas fa-home"></i> Home</a>
            <a href="#" data-section="profile"><i class="fas fa-user"></i> Profile</a>
            <a href="#" data-section="login" id="login-menu-item"><i class="fas fa-sign-in-alt"></i> Login</a>
            <a href="#" data-section="signup" id="signup-menu-item"><i class="fas fa-user-plus"></i> Sign Up</a>
        </nav>
    </div>

    <h3>MAPOVA AI</h3>

    <div id="home" class="content-section active">
        <h2>Welcome to MAPOVA AI</h2>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;margin:15px 0;">
            <div style="background:#2a2a2a;padding:15px;border-radius:10px;border:1px solid #444;">
                <h3 style="color:#00FF88;margin-bottom:10px;text-align:center;">🚀 Smart AI Assistant</h3>
                <p style="color:#ccc;font-size:14px;">Advanced AI powered by Groq for instant responses</p>
            </div>
            <div style="background:#2a2a2a;padding:15px;border-radius:10px;border:1px solid #444;">
                <h3 style="color:#00FF88;margin-bottom:10px;">💬 Real-time Chat</h3>
                <p style="color:#ccc;font-size:14px;">Seamless conversation with instant delivery</p>
            </div>
        </div>
    </div>

    <div id="profile" class="content-section">
        <h2>User Profile</h2>
        <div class="profile-info">
            <div class="profile-details">
                <h3 id="profile-email">User Email</h3>
                <p style="color:#ccc;">Account Status: <span id="verification-status" style="color:#00FF88;">Loading...</span></p>
                <p style="color:#ccc;">Member since: <span id="join-date">Loading...</span></p>
            </div>
            <div class="profile-stats">
                <div class="stat-card"><div class="stat-number" id="chat-count">0</div><div class="stat-label">Chats Today</div></div>
                <div class="stat-card"><div class="stat-number" id="total-chats">0</div><div class="stat-label">Total Chats</div></div>
                <div class="stat-card"><div class="stat-number" id="account-age">0</div><div class="stat-label">Account Days</div></div>
            </div>
        </div>
    </div>

    <div id="login" class="content-section">
        <h2>Login to MAPOVA AI</h2>
        <div class="auth-form">
            <div class="form-group"><label>Email</label><input type="email" id="login-email" placeholder="Enter your email" required></div>
            <div class="form-group"><label>Password</label><input type="password" id="login-password" placeholder="Enter your password" required></div>
            <button class="auth-btn" onclick="loginUser()">Login</button>
            <div class="forgot-password"><a href="#" onclick="showForgotPassword()">Forgot your password?</a></div>
            <div class="auth-switch">Don't have an account? <a href="#" onclick="showSignup()">Sign up here</a></div>
            <div id="login-error" class="error-message" style="display:none;"></div>
        </div>
    </div>

    <div id="signup" class="content-section">
        <h2>Join MAPOVA AI</h2>
        <div class="auth-form">
            <div class="form-group"><label>Email</label><input type="email" id="signup-email" placeholder="Enter your email" required></div>
            <div class="form-group"><label>Password</label><input type="password" id="signup-password" placeholder="Min. 6 characters" required></div>
            <div class="form-group"><label>Confirm Password</label><input type="password" id="signup-confirm-password" placeholder="Confirm password" required></div>
            <button class="auth-btn" onclick="signupUser()">Create Account</button>
            <div class="auth-switch">Already have an account? <a href="#" onclick="showLogin()">Login here</a></div>
            <div id="signup-error" class="error-message" style="display:none;"></div>
            <div id="signup-success" class="success-message" style="display:none;"></div>
        </div>
    </div>

    <div id="forgot-password" class="content-section">
        <h2>Reset Password</h2>
        <div class="auth-form">
            <div class="form-group"><label>Email</label><input type="email" id="reset-email" placeholder="Enter your email" required></div>
            <button class="auth-btn" onclick="sendPasswordResetEmail()">Send Reset Link</button>
            <button class="auth-btn" style="background:#2a2a2a;color:#00FF88;border:1px solid #00FF88;margin-top:10px;" onclick="showLogin()">Back to Login</button>
            <div id="reset-error" class="error-message" style="display:none;"></div>
        </div>
    </div>

    <div class="header">
        <div class="logo">MAPOVA AI</div>
        <div class="status">🟢 ONLINE</div>
        <div class="user-info" id="user-info" style="display:none;">
            <span class="user-email" id="user-email"></span>
            <button class="logout-btn" onclick="logoutUser()">Logout</button>
        </div>
    </div>

    <div class="chat-container">
        <div class="chat-messages" id="chat-messages">
            <div class="message ai-message">🚀 <strong>Welcome to MAPOVA AI!</strong> How can I help you today?</div>
        </div>
        <div class="chat-input-container">
            <input type="text" id="chat-input" placeholder="Message MAPOVA AI..." autocomplete="off">
            <button id="send-btn">Send</button>
        </div>
        <div class="typing-indicator" id="typing-indicator"><div class="typing-dots"><span></span><span></span><span></span></div></div>
    </div>

    <script>
        class MAPOVAAI {
            constructor() {
                this.isLoading = false;
                this.chatInput = document.getElementById('chat-input');
                this.sendBtn = document.getElementById('send-btn');
                this.chatMessages = document.getElementById('chat-messages');
                this.typingIndicator = document.getElementById('typing-indicator');
                this.chatContainer = document.querySelector('.chat-container');
                this.header = document.querySelector('.header');
                this.chatCount = 0;
                this.totalChats = 0;
                this.setupEvents();
                this.setupMenuNavigation();
                this.setupAuthListener();
            }

            setupAuthListener() {
                if (window.firebaseAuth) {
                    window.firebaseAuth.onAuthStateChanged(window.firebaseAuth.auth, (user) => {
                        this.updateUI(user);
                        if (user) this.updateProfileData(user);
                    });
                }
            }

            updateUI(user) {
                const userInfo = document.getElementById('user-info');
                const userEmail = document.getElementById('user-email');
                const loginMenuItem = document.getElementById('login-menu-item');
                const signupMenuItem = document.getElementById('signup-menu-item');

                if (user) {
                    userInfo.style.display = 'flex';
                    userEmail.textContent = user.email;
                    loginMenuItem.style.display = 'none';
                    signupMenuItem.style.display = 'none';
                } else {
                    userInfo.style.display = 'none';
                    loginMenuItem.style.display = 'block';
                    signupMenuItem.style.display = 'block';
                }
            }

            updateProfileData(user) {
                const profileEmail = document.getElementById('profile-email');
                const verificationStatus = document.getElementById('verification-status');
                const joinDate = document.getElementById('join-date');
                const chatCount = document.getElementById('chat-count');
                const totalChats = document.getElementById('total-chats');
                const accountAge = document.getElementById('account-age');

                if (profileEmail) {
                    profileEmail.textContent = user.email;
                    verificationStatus.textContent = user.emailVerified ? 'Verified ✅' : 'Not Verified ❌';
                    verificationStatus.style.color = user.emailVerified ? '#00FF88' : '#ff4757';
                    
                    const joinDateObj = user.metadata?.creationTime ? new Date(user.metadata.creationTime) : new Date();
                    joinDate.textContent = joinDateObj.toLocaleDateString();
                    
                    const today = new Date();
                    const diffDays = Math.ceil((today - joinDateObj) / (1000 * 60 * 60 * 24));
                    accountAge.textContent = diffDays;
                    
                    chatCount.textContent = this.chatCount;
                    totalChats.textContent = this.totalChats;
                }
            }

            setupMenuNavigation() {
                const menuLinks = document.querySelectorAll('.nav-menu a');
                const contentSections = document.querySelectorAll('.content-section');
                const menuToggle = document.getElementById('menu-toggle');

                menuLinks.forEach(link => {
                    link.addEventListener('click', (e) => {
                        e.preventDefault();
                        const targetSection = link.getAttribute('data-section');
                        contentSections.forEach(section => section.classList.remove('active'));
                        document.getElementById(targetSection).classList.add('active');
                        
                        if (targetSection !== 'home') {
                            this.chatContainer.style.display = 'none';
                            this.header.style.display = 'none';
                        } else {
                            this.chatContainer.style.display = 'flex';
                            this.header.style.display = 'flex';
                        }
                        
                        if (window.innerWidth <= 768) menuToggle.checked = false;
                        if (targetSection === 'profile') {
                            const user = window.firebaseAuth.auth.currentUser;
                            if (user) this.updateProfileData(user);
                        }
                    });
                });
            }

            setupEvents() {
                this.sendBtn.addEventListener('click', () => this.sendMessage());
                this.chatInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter') this.sendMessage();
                });
            }

            async sendMessage() {
                const message = this.chatInput.value.trim();
                if (!message || this.isLoading) return;
                this.addMessage(message, 'user');
                this.chatInput.value = '';
                this.chatCount++;
                this.totalChats++;
                this.showTyping();
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                        body: 'message=' + encodeURIComponent(message)
                    });
                    const data = await response.json();
                    this.hideTyping();
                    this.addMessage(data.response, 'ai', true);
                } catch (error) {
                    this.hideTyping();
                    this.addMessage('Sorry, please try again.', 'ai');
                }
            }

            addMessage(text, sender, isHTML = false) {
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                const contentDiv = document.createElement('div');
                if (isHTML) {
                    contentDiv.innerHTML = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                        .replace(/\*(.*?)\*/g, '<em>$1</em>')
                        .replace(/`(.*?)`/g, '<code>$1</code>')
                        .replace(/\n\n/g, '</p><p>')
                        .replace(/\n/g, '<br>');
                } else {
                    contentDiv.textContent = text;
                }
                messageDiv.appendChild(contentDiv);
                this.chatMessages.appendChild(messageDiv);
                this.scrollToBottom();
            }

            showTyping() { this.typingIndicator.style.display = 'block'; this.scrollToBottom(); }
            hideTyping() { this.typingIndicator.style.display = 'none'; }
            scrollToBottom() { this.chatMessages.scrollTop = this.chatMessages.scrollHeight; }
        }

        function showLogin() { showSection('login'); }
        function showSignup() { showSection('signup'); }
        function showForgotPassword() { showSection('forgot-password'); }
        function showSection(section) {
            document.querySelectorAll('.content-section').forEach(s => s.classList.remove('active'));
            document.getElementById(section).classList.add('active');
        }

        async function signupUser() {
            const email = document.getElementById('signup-email').value;
            const password = document.getElementById('signup-password').value;
            const confirmPassword = document.getElementById('signup-confirm-password').value;
            const errorDiv = document.getElementById('signup-error');
            const successDiv = document.getElementById('signup-success');

            errorDiv.style.display = 'none';
            successDiv.style.display = 'none';

            if (password !== confirmPassword) {
                errorDiv.textContent = 'Passwords do not match!';
                errorDiv.style.display = 'block';
                return;
            }

            try {
                const userCredential = await window.firebaseAuth.createUserWithEmailAndPassword(window.firebaseAuth.auth, email, password);
                await window.firebaseAuth.sendEmailVerification(userCredential.user);
                successDiv.innerHTML = `🎉 Account created! Verification email sent to ${email}`;
                successDiv.style.display = 'block';
                setTimeout(() => showSection('home'), 3000);
            } catch (error) {
                errorDiv.textContent = error.message;
                errorDiv.style.display = 'block';
            }
        }

        async function loginUser() {
            const email = document.getElementById('login-email').value;
            const password = document.getElementById('login-password').value;
            const errorDiv = document.getElementById('login-error');

            errorDiv.style.display = 'none';

            try {
                await window.firebaseAuth.signInWithEmailAndPassword(window.firebaseAuth.auth, email, password);
                showSection('home');
            } catch (error) {
                errorDiv.textContent = error.message;
                errorDiv.style.display = 'block';
            }
        }

        async function sendPasswordResetEmail() {
            const email = document.getElementById('reset-email').value;
            const errorDiv = document.getElementById('reset-error');

            errorDiv.style.display = 'none';

            try {
                await window.firebaseAuth.sendPasswordResetEmail(window.firebaseAuth.auth, email);
                alert('Password reset email sent! Check your inbox.');
                showSection('login');
            } catch (error) {
                errorDiv.textContent = error.message;
                errorDiv.style.display = 'block';
            }
        }

        async function logoutUser() {
            try {
                await window.firebaseAuth.signOut(window.firebaseAuth.auth);
                showSection('home');
            } catch (error) {
                console.error('Logout error:', error);
            }
        }

        document.addEventListener('DOMContentLoaded', () => new MAPOVAAI());
    </script>
</body>
</html>
"""

class ForeverAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = GROQ_API_URL
    
    def get_response(self, message):
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "messages": [{"role": "user", "content": message}],
                "model": "llama-3.1-8b-instant",
                "temperature": 0.7,
                "max_tokens": 1024,
                "top_p": 1
            }
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return "🔄 MAPOVA AI is reconnecting... Please try again!"
        except Exception:
            return "🚀 MAPOVA AI is here! What can I help you with?"

def run_server():
    PORT = 7080
    ai = ForeverAI(GROQ_API_KEY)
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(HTML_CONTENT.encode())
            else:
                super().do_GET()
        
        def do_POST(self):
            if self.path == '/api/chat':
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')
                message = urllib.parse.parse_qs(post_data).get('message', [''])[0]
                response = ai.get_response(message)
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"response": response}).encode())
            else:
                self.send_response(404)
                self.end_headers()
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🎯 MAPOVA AI Running: http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()