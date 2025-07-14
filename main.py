#!/usr/bin/env python3
"""
Bluetooth Chat Application - Main Launcher
Aplikasi chat dan transfer file menggunakan koneksi Bluetooth
Author: Terminal Chat Bluetooth
"""

import sys
import os
from colorama import init, Fore, Style

# Initialize colorama
init()

def show_menu():
    """Menampilkan menu utama"""
    print(f"{Fore.BLUE}╔══════════════════════════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║              BLUETOOTH CHAT APPLICATION              ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}║            Chat & File Transfer via Bluetooth       ║{Style.RESET_ALL}")
    print(f"{Fore.BLUE}╚══════════════════════════════════════════════════════╝{Style.RESET_ALL}")
    print()
    print(f"{Fore.GREEN}Pilih mode aplikasi:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  1. Server Mode - Menunggu koneksi dari client{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  2. Client Mode - Terhubung ke server{Style.RESET_ALL}")
    print(f"{Fore.CYAN}  3. Keluar{Style.RESET_ALL}")
    print()

def main():
    """Fungsi utama aplikasi"""
    while True:
        show_menu()
        
        try:
            choice = input(f"{Fore.YELLOW}Masukkan pilihan (1-3): {Style.RESET_ALL}")
            
            if choice == '1':
                print(f"{Fore.GREEN}🚀 Memulai Server Mode...{Style.RESET_ALL}")
                print()
                os.system('python3 server.py')
                
            elif choice == '2':
                print(f"{Fore.GREEN}🚀 Memulai Client Mode...{Style.RESET_ALL}")
                print()
                os.system('python3 client.py')
                
            elif choice == '3':
                print(f"{Fore.YELLOW}👋 Selamat tinggal!{Style.RESET_ALL}")
                sys.exit(0)
                
            else:
                print(f"{Fore.RED}❌ Pilihan tidak valid. Silakan coba lagi.{Style.RESET_ALL}")
                input(f"{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")
                
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Selamat tinggal!{Style.RESET_ALL}")
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
            input(f"{Fore.YELLOW}Tekan Enter untuk melanjutkan...{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
