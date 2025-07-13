@echo off
REM Bluetooth Pairing Script untuk Windows

echo === BLUETOOTH PAIRING WINDOWS ===
echo Script untuk pairing perangkat Bluetooth di Windows
echo.

echo 1. Pastikan Bluetooth sudah enabled di Windows Settings
echo 2. Buka Settings > Devices > Bluetooth ^& other devices
echo 3. Atau gunakan PowerShell commands berikut:
echo.

echo === POWERSHELL COMMANDS ===
echo Buka PowerShell sebagai Administrator dan jalankan:
echo.
echo # Cek status Bluetooth
echo Get-PnpDevice -Class Bluetooth
echo.
echo # Enable Bluetooth jika disabled
echo Enable-PnpDevice -InstanceId "BTHUSB\..."
echo.
echo # Scan dan pair perangkat
echo Add-Type -AssemblyName System.Runtime.WindowsRuntime
echo $asTaskGeneric = ([System.WindowsRuntimeSystemExtensions].GetMethods() ^| ? { $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
echo Function Await($WinRtTask, $ResultType) {
echo     $asTask = $asTaskGeneric.MakeGenericMethod($ResultType)
echo     $netTask = $asTask.Invoke($null, @($WinRtTask))
echo     $netTask.Wait(-1) ^| Out-Null
echo     $netTask.Result
echo }
echo [Windows.Devices.Bluetooth.BluetoothAdapter,Windows.Devices.Bluetooth,ContentType=WindowsRuntime] ^| Out-Null
echo $adapter = Await ([Windows.Devices.Bluetooth.BluetoothAdapter]::GetDefaultAsync()) ([Windows.Devices.Bluetooth.BluetoothAdapter])
echo if ($adapter) { 
echo     "Bluetooth adapter ditemukan"
echo     "Radio status: " + $adapter.IsLowEnergySupported
echo } else {
echo     "Bluetooth adapter tidak ditemukan"
echo }
echo.

echo === MANUAL PAIRING ===
echo 1. Buka Settings (Windows + I)
echo 2. Pilih Devices
echo 3. Pilih Bluetooth ^& other devices  
echo 4. Klik "Add Bluetooth or other device"
echo 5. Pilih "Bluetooth"
echo 6. Pilih perangkat target dari daftar
echo 7. Ikuti instruksi pairing
echo.

echo === COMMAND LINE PAIRING ===
echo Untuk pairing via command line, install BTStackCLI:
echo 1. Download BTStackCLI dari GitHub
echo 2. Extract ke folder
echo 3. Gunakan commands:
echo    BTStack.exe scan
echo    BTStack.exe pair MAC_ADDRESS
echo.

echo === ALTERNATIVE MENGGUNAKAN NETSH ===
echo # Lihat adapter Bluetooth
echo netsh interface show interface
echo.
echo # Enable/disable Bluetooth (jika ada)
echo netsh interface set interface "Bluetooth Network Connection" enabled
echo.

echo === TROUBLESHOOTING ===
echo Jika gagal:
echo 1. Restart Windows Bluetooth Service:
echo    - Buka Services.msc
echo    - Cari "Bluetooth Support Service"  
echo    - Restart service
echo 2. Update driver Bluetooth di Device Manager
echo 3. Hapus pairing lama dari Settings
echo 4. Coba pairing ulang
echo.

pause
