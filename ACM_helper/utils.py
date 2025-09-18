# 在此处编写辅助工具函数 
# 例如：输入输出处理、调试工具、性能测试等 
import subprocess
import os
import sys
import zipfile

class Make_Test_Cases_Cpp:
    @staticmethod
    def clean_up(std_cpp_path="std.cpp", gen_cpp_path="gen.cpp"):
        """清理生成的可执行文件"""
        std_exe_name = os.path.splitext(os.path.basename(std_cpp_path))[0] + ".exe"
        gen_exe_name = os.path.splitext(os.path.basename(gen_cpp_path))[0] + ".exe"
        
        if os.path.exists(std_exe_name):
            os.remove(std_exe_name)
        if os.path.exists(gen_exe_name):
            os.remove(gen_exe_name)
        print("已清理临时文件")

    @staticmethod
    def generate_test_cases(L, R, std_cpp_path="std.cpp", gen_cpp_path="gen.cpp"):
        # 确保必要的文件存在
        if not os.path.exists(std_cpp_path):
            print(f"错误：未找到 {std_cpp_path}")
            return
        
        if not os.path.exists(gen_cpp_path):
            print(f"错误：未找到 {gen_cpp_path}")
            return
        
        # 创建data文件夹（如果不存在）
        if not os.path.exists("data"):
            os.makedirs("data")
            print("创建data文件夹")
        
        # 编译标准程序和生成器
        print("正在编译程序...")
        
        # 从文件路径提取文件名（不含扩展名）用于生成可执行文件名
        std_exe_name = os.path.splitext(os.path.basename(std_cpp_path))[0] + ".exe"
        gen_exe_name = os.path.splitext(os.path.basename(gen_cpp_path))[0] + ".exe"
        
        compile_std = subprocess.run(["g++", std_cpp_path, "-o", std_exe_name, "-O2", "-std=c++11"])
        if compile_std.returncode != 0:
            print(f"编译 {std_cpp_path} 失败")
            return
        
        compile_gen = subprocess.run(["g++", gen_cpp_path, "-o", gen_exe_name, "-O2", "-std=c++11"])
        if compile_gen.returncode != 0:
            print(f"编译 {gen_cpp_path} 失败")
            return
        
        # 生成测试用例
        for i in range(L, R + 1):
            print(f"正在生成测试用例 {i}...")
            
            # 生成输入数据
            input_filename = os.path.join("data", f"case{i}.in.in")
            with open(input_filename, "w") as f:
                # 运行生成器，将输出重定向到文件
                subprocess.run([f"./{gen_exe_name}"], stdout=f)
            
            # 生成输出数据
            output_filename = os.path.join("data", f"case{i}.out.out")
            with open(input_filename, "r") as fin, open(output_filename, "w") as fout:
                # 运行标准程序，将输入重定向从文件，输出重定向到文件
                subprocess.run([f"./{std_exe_name}"], stdin=fin, stdout=fout)
        
        Make_Test_Cases_Cpp.clean_up(std_cpp_path, gen_cpp_path)
        print(f"成功生成测试用例 {L} 到 {R}，文件保存在data文件夹中")

    @staticmethod
    def create_zip_archive():
        """将data文件夹中的文件直接压缩到zip根目录"""
        zip_filename = "test_cases.zip"
        
        if not os.path.exists("data"):
            print("data文件夹不存在，无法创建压缩文件")
            return False
        
        if not os.listdir("data"):
            print("data文件夹为空，无法创建压缩文件")
            return False
        
        try:
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file in os.listdir("data"):
                    file_path = os.path.join("data", file)
                    if os.path.isfile(file_path):
                        # 直接将文件添加到zip根目录，不保留data文件夹结构
                        zipf.write(file_path, file)
            
            print(f"成功创建压缩文件: {zip_filename}")
            print(f"压缩文件大小: {os.path.getsize(zip_filename) / 1024:.2f} KB")
            print("解压后文件结构:")
            print("case1.in.in")
            print("case1.out.out")
            print("case2.in.in")
            print("case2.out.out")
            print("...")
            return True
        except Exception as e:
            print(f"创建压缩文件时出错: {e}")
            return False

if __name__ == "__main__":
    # 测试代码示例
    print("=== 测试 Make_Test_Cases_Cpp 类 ===")
    
    # 测试清理功能
    print("\n1. 测试清理功能...")
    # 创建两个临时文件模拟需要清理的文件
    with open("std.exe", "w") as f:
        f.write("temp")
    with open("gen.exe", "w") as f:
        f.write("temp")
    
    print("创建临时文件 std.exe 和 gen.exe")
    Make_Test_Cases_Cpp.clean_up()
    print("清理完成")
    
    # 测试生成测试用例功能 (需要实际有std.cpp和gen.cpp文件)
    print("\n2. 测试生成测试用例功能...")
    if os.path.exists("std.cpp") and os.path.exists("gen.cpp"):
        try:
            # 生成1个测试用例
            Make_Test_Cases_Cpp.generate_test_cases(1, 1)
            print("生成测试用例完成")
        except Exception as e:
            print(f"生成测试用例时出错: {e}")
    else:
        print("未找到std.cpp或gen.cpp，跳过生成测试用例测试")
    
    # 测试创建压缩文件功能
    print("\n3. 测试创建压缩文件功能...")
    if os.path.exists("data") and os.listdir("data"):
        success = Make_Test_Cases_Cpp.create_zip_archive()
        if success:
            print("压缩文件创建成功")
        else:
            print("压缩文件创建失败")
    else:
        print("data文件夹不存在或为空，跳过压缩文件测试")
    
    print("\n=== 测试完成 ===")