     .section .rodata
     .global termux_bootstrap_zip_start
     .global termux_bootstrap_zip_end

     termux_bootstrap_zip_start:
         .incbin "bootstrap-aarch64.zip"
     termux_bootstrap_zip_end:
