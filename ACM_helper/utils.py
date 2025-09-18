import subprocess
import os
import sys
import zipfile

class MakeTestCasesCpp:
    """
    用于生成和管理 C++ 测试用例的工具类。
    包含清理、生成测试用例、压缩数据等功能。
    """

    @staticmethod
    def clean_up(std_cpp_path="std.cpp", gen_cpp_path="gen.cpp"):
        """
        清理生成的可执行文件。
        """
        std_exe_name = os.path.splitext(os.path.basename(std_cpp_path))[0] + ".exe"
        gen_exe_name = os.path.splitext(os.path.basename(gen_cpp_path))[0] + ".exe"
        if os.path.exists(std_exe_name):
            os.remove(std_exe_name)
        if os.path.exists(gen_exe_name):
            os.remove(gen_exe_name)
        print("已清理临时文件")

    @staticmethod
    def generate_test_cases(L, R, std_cpp_path="std.cpp", gen_cpp_path="gen.cpp"):
        """
        批量生成测试用例，输入为生成区间 L~R。
        依赖 std.cpp（标准程序）和 gen.cpp（数据生成器）。
        """
        if not os.path.exists(std_cpp_path):
            print(f"错误：未找到 {std_cpp_path}")
            return
        if not os.path.exists(gen_cpp_path):
            print(f"错误：未找到 {gen_cpp_path}")
            return
        if not os.path.exists("data"):
            os.makedirs("data")
            print("创建data文件夹")
        print("正在编译程序...")
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
        for i in range(L, R + 1):
            print(f"正在生成测试用例 {i}...")
            input_filename = os.path.join("data", f"case{i}.in.in")
            with open(input_filename, "w") as f:
                subprocess.run([f"./{gen_exe_name}"], stdout=f)
            output_filename = os.path.join("data", f"case{i}.out.out")
            with open(input_filename, "r") as fin, open(output_filename, "w") as fout:
                subprocess.run([f"./{std_exe_name}"], stdin=fin, stdout=fout)
        MakeTestCasesCpp.clean_up(std_cpp_path, gen_cpp_path)
        print(f"成功生成测试用例 {L} 到 {R}，文件保存在data文件夹中")

    @staticmethod
    def create_zip_archive():
        """
        将 data 文件夹中的文件压缩到 zip 根目录。
        """
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
    print("=== 测试 MakeTestCasesCpp 类 ===")
    print("\n1. 测试清理功能...")
    with open("std.exe", "w") as f:
        f.write("temp")
    with open("gen.exe", "w") as f:
        f.write("temp")
    print("创建临时文件 std.exe 和 gen.exe")
    MakeTestCasesCpp.clean_up()
    print("清理完成")
    print("\n2. 测试生成测试用例功能...")
    if os.path.exists("std.cpp") and os.path.exists("gen.cpp"):
        try:
            MakeTestCasesCpp.generate_test_cases(1, 1)
            print("生成测试用例完成")
        except Exception as e:
            print(f"生成测试用例时出错: {e}")
    else:
        print("未找到std.cpp或gen.cpp，跳过生成测试用例测试")
    print("\n3. 测试创建压缩文件功能...")
    if os.path.exists("data") and os.listdir("data"):
        success = MakeTestCasesCpp.create_zip_archive()
        if success:
            print("压缩文件创建成功")
        else:
            print("压缩文件创建失败")
    else:
        print("data文件夹不存在或为空，跳过压缩文件测试")
    print("\n=== 测试完成 ===")