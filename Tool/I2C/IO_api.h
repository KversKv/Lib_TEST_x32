#ifndef IO_api_h
#define IO_api_h
#include <windows.h>

#ifndef _DLL_API  
#define _DLL_API _declspec(dllexport)  
#else  
#define _DLL_API _declspec(dllimport)  
#endif

//interface读写接口(8位寄存器)
_DLL_API int WINAPI I2C_read_reg(int device_addr, int reg_addr);
_DLL_API int WINAPI I2C_write_reg(int device_addr, int reg_addr, int data_need_to_be_written);

//2003/2002/2005芯片interface读写接口(10位寄存器)
_DLL_API int WINAPI I2C_read_reg_2003(int device_addr, int reg_addr);
_DLL_API int WINAPI I2C_write_reg_2003(int device_addr, int reg_addr, int data_need_to_be_written);

//大数字读写接口
_DLL_API int WINAPI I2C_read_data(int device_addr, int reg_addr);
_DLL_API int WINAPI I2C_write_data(int device_addr, int reg_addr, int data_need_to_be_written);

//efuse所有芯片都不同
//2003 EFUSE读写接口
_DLL_API int WINAPI efs_read_reg_2003 (int device_addr, int gui_reg_addr);
_DLL_API int WINAPI efs_write_reg_2003(int device_addr, int gui_reg_addr, int gui_data_to_be_written);

//1600 EFUSE读写接口
_DLL_API int WINAPI efs_read_reg_1600 (int device_addr, int gui_reg_addr);
_DLL_API int WINAPI efs_write_reg_1600(int device_addr, int gui_reg_addr, int gui_data_to_be_written);

//1501p EFUSE读写接口
_DLL_API int WINAPI efs_read_reg_1501p (int device_addr, int gui_reg_addr);
_DLL_API int WINAPI efs_write_reg_1501p(int device_addr, int gui_reg_addr, int gui_data_to_be_written);

//2002 EFUSE读写接口
_DLL_API int WINAPI efs_read_reg_2002 (int device_addr, int gui_reg_addr);
_DLL_API int WINAPI efs_write_reg_2002(int device_addr, int gui_reg_addr, int gui_data_to_be_written);

//1306 EFUSE读写接口
_DLL_API int WINAPI efs_read_reg_1306 (int device_addr, int gui_reg_addr);
_DLL_API int WINAPI efs_write_reg_1306(int device_addr, int gui_reg_addr, int gui_data_to_be_written);

//1502 EFUSE读写接口
_DLL_API int WINAPI efs_read_reg_1502 (int device_addr, int gui_reg_addr);
_DLL_API int WINAPI efs_write_reg_1502(int device_addr, int gui_reg_addr, int gui_data_to_be_written);

#endif//IO_api_h
