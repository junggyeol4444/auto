"""
Smart Video Editor Pro - Main Application
"""
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QWidget, 
                             QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QLineEdit, QTextEdit, QFileDialog, QProgressBar,
                             QComboBox, QMessageBox, QGroupBox, QCheckBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.video_downloader import VideoDownloader
from core.style_learner import StyleLearner
from core.video_editor import VideoEditor
from database.models import Database


class WorkerThread(QThread):
    """Worker thread for background tasks"""
    progress = pyqtSignal(str, float)
    finished = pyqtSignal(object)
    error = pyqtSignal(str)
    
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class LearningTab(QWidget):
    """Tab for learning editing styles from YouTube videos"""
    
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.downloader = VideoDownloader()
        self.learner = StyleLearner(database)
        self.worker = None
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Learn Editing Style from YouTube Videos")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # YouTube URL input
        url_group = QGroupBox("YouTube Video")
        url_layout = QVBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube video URL...")
        url_layout.addWidget(QLabel("Video URL:"))
        url_layout.addWidget(self.url_input)
        
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)
        
        # Profile name input
        profile_group = QGroupBox("Profile Settings")
        profile_layout = QVBoxLayout()
        
        self.profile_input = QLineEdit()
        self.profile_input.setPlaceholderText("Enter profile name...")
        profile_layout.addWidget(QLabel("Profile Name:"))
        profile_layout.addWidget(self.profile_input)
        
        profile_group.setLayout(profile_layout)
        layout.addWidget(profile_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.download_btn = QPushButton("Download Video")
        self.download_btn.clicked.connect(self.download_video)
        button_layout.addWidget(self.download_btn)
        
        self.learn_btn = QPushButton("Learn Style")
        self.learn_btn.clicked.connect(self.learn_style)
        self.learn_btn.setEnabled(False)
        button_layout.addWidget(self.learn_btn)
        
        layout.addLayout(button_layout)
        
        # Progress
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # Status/Log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log_text)
        
        layout.addStretch()
        self.setLayout(layout)
        
        self.downloaded_video_path = None
    
    def log(self, message):
        """Add message to log"""
        self.log_text.append(message)
    
    def download_video(self):
        """Download YouTube video"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL")
            return
        
        self.log(f"Starting download: {url}")
        self.download_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        def progress_hook(d):
            if d['status'] == 'downloading':
                try:
                    percent = float(d['_percent_str'].strip('%'))
                    self.progress_bar.setValue(int(percent))
                except:
                    pass
        
        def download_task():
            return self.downloader.download_video(url, progress_callback=progress_hook)
        
        self.worker = WorkerThread(download_task)
        self.worker.finished.connect(self.on_download_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_download_finished(self, video_path):
        """Handle download completion"""
        self.downloaded_video_path = video_path
        self.log(f"Download complete: {video_path}")
        self.download_btn.setEnabled(True)
        self.learn_btn.setEnabled(True)
        self.progress_bar.setValue(100)
    
    def learn_style(self):
        """Learn editing style from video"""
        if not self.downloaded_video_path:
            QMessageBox.warning(self, "Error", "Please download a video first")
            return
        
        profile_name = self.profile_input.text().strip()
        if not profile_name:
            QMessageBox.warning(self, "Error", "Please enter a profile name")
            return
        
        self.log(f"Learning style from video...")
        self.learn_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        def progress_callback(message, progress):
            self.worker.progress.emit(message, progress)
        
        def learn_task():
            return self.learner.learn_from_video(
                self.downloaded_video_path, 
                profile_name,
                progress_callback
            )
        
        self.worker = WorkerThread(learn_task)
        self.worker.progress.connect(self.on_learning_progress)
        self.worker.finished.connect(self.on_learning_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_learning_progress(self, message, progress):
        """Handle learning progress"""
        self.log(message)
        self.progress_bar.setValue(int(progress * 100))
    
    def on_learning_finished(self, results):
        """Handle learning completion"""
        self.log("Learning complete!")
        self.log(f"Detected {results['scene_stats']['total_scenes']} scenes")
        self.log(f"Detected {results['audio_stats']['total_voice_segments']} voice segments")
        self.learn_btn.setEnabled(True)
        self.progress_bar.setValue(100)
        QMessageBox.information(self, "Success", "Style learning completed successfully!")
    
    def on_error(self, error_msg):
        """Handle errors"""
        self.log(f"ERROR: {error_msg}")
        self.download_btn.setEnabled(True)
        self.learn_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", error_msg)


class EditingTab(QWidget):
    """Tab for editing videos using learned styles"""
    
    def __init__(self, database):
        super().__init__()
        self.database = database
        self.editor = VideoEditor()
        self.learner = StyleLearner(database)
        self.worker = None
        
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Edit Video with Learned Style")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(title)
        
        # Input video
        input_group = QGroupBox("Input Video")
        input_layout = QVBoxLayout()
        
        input_file_layout = QHBoxLayout()
        self.input_path = QLineEdit()
        self.input_path.setReadOnly(True)
        input_file_layout.addWidget(self.input_path)
        
        browse_input_btn = QPushButton("Browse...")
        browse_input_btn.clicked.connect(self.browse_input)
        input_file_layout.addWidget(browse_input_btn)
        
        input_layout.addWidget(QLabel("Input Video:"))
        input_layout.addLayout(input_file_layout)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Profile selection
        profile_group = QGroupBox("Editing Profile")
        profile_layout = QVBoxLayout()
        
        self.profile_combo = QComboBox()
        self.refresh_profiles()
        profile_layout.addWidget(QLabel("Select Profile:"))
        profile_layout.addWidget(self.profile_combo)
        
        refresh_btn = QPushButton("Refresh Profiles")
        refresh_btn.clicked.connect(self.refresh_profiles)
        profile_layout.addWidget(refresh_btn)
        
        profile_group.setLayout(profile_layout)
        layout.addWidget(profile_group)
        
        # Options
        options_group = QGroupBox("Editing Options")
        options_layout = QVBoxLayout()
        
        self.remove_silence_check = QCheckBox("Remove Silence")
        self.remove_silence_check.setChecked(True)
        options_layout.addWidget(self.remove_silence_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        # Output video
        output_group = QGroupBox("Output Video")
        output_layout = QVBoxLayout()
        
        output_file_layout = QHBoxLayout()
        self.output_path = QLineEdit()
        output_file_layout.addWidget(self.output_path)
        
        browse_output_btn = QPushButton("Browse...")
        browse_output_btn.clicked.connect(self.browse_output)
        output_file_layout.addWidget(browse_output_btn)
        
        output_layout.addWidget(QLabel("Output Video:"))
        output_layout.addLayout(output_file_layout)
        
        output_group.setLayout(output_layout)
        layout.addWidget(output_group)
        
        # Edit button
        self.edit_btn = QPushButton("Edit Video")
        self.edit_btn.clicked.connect(self.edit_video)
        layout.addWidget(self.edit_btn)
        
        # Progress
        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)
        
        # Status/Log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(QLabel("Log:"))
        layout.addWidget(self.log_text)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def log(self, message):
        """Add message to log"""
        self.log_text.append(message)
    
    def refresh_profiles(self):
        """Refresh the profile list"""
        self.profile_combo.clear()
        profiles = self.database.get_all_profiles()
        for profile in profiles:
            self.profile_combo.addItem(profile.name)
    
    def browse_input(self):
        """Browse for input video"""
        filename, _ = QFileDialog.getOpenFileName(
            self, "Select Input Video", "", 
            "Video Files (*.mp4 *.avi *.mkv *.mov *.flv);;All Files (*)"
        )
        if filename:
            self.input_path.setText(filename)
            # Auto-suggest output path
            if not self.output_path.text():
                base, ext = os.path.splitext(filename)
                self.output_path.setText(f"{base}_edited{ext}")
    
    def browse_output(self):
        """Browse for output video"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Save Output Video", "", 
            "Video Files (*.mp4);;All Files (*)"
        )
        if filename:
            self.output_path.setText(filename)
    
    def edit_video(self):
        """Edit video using selected profile"""
        input_path = self.input_path.text().strip()
        output_path = self.output_path.text().strip()
        profile_name = self.profile_combo.currentText()
        
        if not input_path:
            QMessageBox.warning(self, "Error", "Please select an input video")
            return
        
        if not output_path:
            QMessageBox.warning(self, "Error", "Please specify an output path")
            return
        
        if not profile_name:
            QMessageBox.warning(self, "Error", "Please select a profile")
            return
        
        self.log(f"Starting video editing with profile: {profile_name}")
        self.edit_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        def progress_callback(message, progress):
            self.worker.progress.emit(message, progress)
        
        def edit_task():
            patterns = self.learner.get_profile_patterns(profile_name)
            if not patterns:
                raise Exception(f"Profile '{profile_name}' not found")
            
            return self.editor.edit_video(
                input_path,
                output_path,
                patterns,
                remove_silence_enabled=self.remove_silence_check.isChecked(),
                progress_callback=progress_callback
            )
        
        self.worker = WorkerThread(edit_task)
        self.worker.progress.connect(self.on_editing_progress)
        self.worker.finished.connect(self.on_editing_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_editing_progress(self, message, progress):
        """Handle editing progress"""
        self.log(message)
        self.progress_bar.setValue(int(progress * 100))
    
    def on_editing_finished(self, output_path):
        """Handle editing completion"""
        self.log(f"Video editing complete: {output_path}")
        self.edit_btn.setEnabled(True)
        self.progress_bar.setValue(100)
        QMessageBox.information(self, "Success", f"Video edited successfully!\n\nOutput: {output_path}")
    
    def on_error(self, error_msg):
        """Handle errors"""
        self.log(f"ERROR: {error_msg}")
        self.edit_btn.setEnabled(True)
        QMessageBox.critical(self, "Error", error_msg)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize database
        self.database = Database()
        
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Smart Video Editor Pro")
        self.setGeometry(100, 100, 900, 700)
        
        # Create tab widget
        tabs = QTabWidget()
        
        # Add tabs
        tabs.addTab(LearningTab(self.database), "Learn Style")
        tabs.addTab(EditingTab(self.database), "Edit Video")
        
        self.setCentralWidget(tabs)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
