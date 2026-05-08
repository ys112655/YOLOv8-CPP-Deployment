# === Build Output ===
build/
out/
cmake-build-*/
*.vcxproj*
*.sln
*.suo
*.user
*.useros
*.userprefs
CMakeCache.txt
CMakeFiles/
cmake_install.cmake
Makefile
.ninja*
*.log

# === Model Files (huge) ===
*.onnx
*.pt
*.pth
*.weights
*.engine
*.trt
*.onnx_data
*.onnxruntime*

# === Binaries & Libraries ===
*.exe
*.dll
*.lib
*.dylib
*.so
*.a
*.exp
*.pdb
*.ilk
*.obj
*.o

# === IDE & Editor ===
.vs/
.idea/
.vscode/
*.swp
*.swo
*~
.DS_Store
Thumbs.db

# === Python artifacts (if any) ===
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
*.egg
.eggs/

# === OS junk ===
*.bak
*.tmp

git init; git add .; git commit -m "feat: init YOLOv8 C++ real-time deployment engine"; git branch -M main; git remote add origin [此处替换为我的仓库链接]; git push -u origin main

