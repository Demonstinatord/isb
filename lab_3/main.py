import argparse
import os

from asymmetric_crypt import Asymmetrical
from sup_functions import SupportFunctions
from symmetric_crypt import Symmetric
from file_manager import FileManager


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-gen', '--generation',
                       help='Запускает режим генерации ключей')
    parser.add_argument('-enc', '--encryption',
                       help='Запускает режим шифрования')
    parser.add_argument('-dec', '--decryption',
                       help='Запускает режим дешифрования')
    args = parser.parse_args()
    json_path = None
    if args.generation is not None:
        json_path = args.generation
        settings_generation = FileManager.load_config_settings(json_path if isinstance(json_path, str) else None)
    if args.encryption is not None:
        json_path = args.encryption
        settings_encryption = FileManager.load_config_settings(json_path if isinstance(json_path, str) else None)
    if args.decryption is not None:
        json_path = args.decryption
        settings_decryption = FileManager.load_config_settings(json_path if isinstance(json_path, str) else None)


    if args.generation is not None:
        public_key, private_key, encrypted_symmetric_key = SupportFunctions.generate_keys(settings_generation)
        FileManager.save_public_key(public_key, settings_generation['public_key'])
        FileManager.save_private_key(private_key, settings_generation['secret_key'])
        FileManager.save_encrypt_symmetric_key(encrypted_symmetric_key, settings_generation)
    if args.encryption is not None:
        print("\n||Шифрование информации с помощью алгоритма SM4||")
        path_to_initial = settings_encryption['initial_file']
        path_to_private_key = settings_encryption['secret_key']
        path_to_encrypted_sym_key = settings_encryption['encrypted_symmetric_key_file']
        encrypted_file_path = settings_encryption['encrypted_file']
        if not path_to_encrypted_sym_key:
            path_to_encrypted_sym_key = settings_encryption['symmetric_key']
        if not all([path_to_initial, path_to_private_key,
                    path_to_encrypted_sym_key, encrypted_file_path]):
            print(
                "Error: Не указаны все необходимые пути в настройках для шифрования.")
            exit(1)
        if not os.path.exists(path_to_initial):
            print(f"Error: Исходный файл не найден по пути {path_to_initial}")
            exit(1)
        if not os.path.exists(path_to_private_key):
            print(
                f"Error: Файл приватного ключа не найден по пути {path_to_private_key}")
            exit(1)
        if not os.path.exists(path_to_encrypted_sym_key):
            print(
                f"Error: Файл зашифрованного симметричного ключа не найден по пути {path_to_encrypted_sym_key}")
            exit(1)
        private_key = FileManager.read_private_key(path_to_private_key)
        encrypted_sym_key_data = FileManager.read_file(path_to_encrypted_sym_key)
        symmetric_key = Asymmetrical.decrypt_symmetric_key(private_key, encrypted_sym_key_data)
        print(f"Чтение файла {path_to_initial}...")
        content = FileManager.read_file(path_to_initial)

        ciphertext = Symmetric.text_encrypter(content, symmetric_key)

        print(f"Сохранение зашифрованных данных в файл {encrypted_file_path}...")
        FileManager.write_file(encrypted_file_path, ciphertext)

        print("||Шифрование и сохранение завершено успешно!||")
    if args.decryption is not None:
        print("\n||Дешифрование информации с помощью алгоритма SM4||")
        path_to_encrypt_file = settings_decryption['encrypted_file']
        path_to_private_key = settings_decryption['secret_key']
        path_to_encrypted_sym_key = settings_decryption['encrypted_symmetric_key_file'] or \
                                    settings_decryption['symmetric_key']
        path_to_decrypted_key = settings_decryption['decrypted_file']

        if not all([path_to_encrypt_file, path_to_private_key,
                    path_to_encrypted_sym_key, path_to_decrypted_key]):
            print(
                "Error: Не указаны все необходимые пути в настройках для дешифрования.")
            exit(1)
        if not os.path.exists(path_to_encrypt_file):
            print(
                f"Error: Зашифрованный файл не найден по пути {path_to_encrypt_file}")
            exit(1)
        if not os.path.exists(path_to_private_key):
            print(
                f"Error: Файл приватного ключа не найден по пути {path_to_private_key}")
            exit(1)
        if not os.path.exists(path_to_encrypted_sym_key):
            print(
                f"Error: Файл зашифрованного симметричного ключа не найден по пути {path_to_encrypted_sym_key}")
            exit(1)

        private_key = FileManager.read_private_key(path_to_private_key)
        encrypted_sym_key_data = FileManager.read_file(path_to_encrypted_sym_key)
        symmetric_key = Asymmetrical.decrypt_symmetric_key(private_key, encrypted_sym_key_data)
        print(f"Чтение зашифрованного файла {path_to_encrypt_file}...")
        encrypted_content = FileManager.read_file(path_to_encrypt_file)


        plaintext = Symmetric.text_decrypter(encrypted_content, symmetric_key)

        print(f"Сохранение расшифрованных данных в {path_to_decrypted_key}...")
        FileManager.write_file(path_to_decrypted_key, plaintext)
        print("||Дешифрование и сохранение завершено успешно!||")

if __name__ == "__main__":
        main()

