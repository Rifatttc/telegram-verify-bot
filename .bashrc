clear
echo -e "\e[1;32m  ____  _  __       _     __  __ _____ _   _ "
echo -e "\e[1;32m |  _ \(_)/ _| __ _| |_  |  \/  | ____| | | |"
echo -e "\e[1;32m | |_) | | |_ / _` | __| | |\/| |  _| | | | |"
echo -e "\e[1;32m |  _ <| |  _| (_| | |_  | |  | | |___| |_| |"
echo -e "\e[1;32m |_| \_\_|_|  \__,_|\__| |_|  |_|_____|\___/ "
echo -e "\e[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\e[0m"
echo -e "\e[1;33m  [1] Run Telegram Verify Bot"
echo -e "\e[1;33m  [2] Update/Push to GitHub"
echo -e "\e[1;33m  [3] Termux Storage Setup"
echo -e "\e[1;31m  [4] Exit Termux"
echo -e "\e[1;34m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\e[0m"

read -p " Select an option [1-4]: " choice

case $choice in
    1)
        python verify.py
        ;;
    2)
        git add . && git commit -m "update" && git push origin main
        ;;
    3)
        termux-setup-storage
        ;;
    4)
        exit
        ;;
    *)
        echo "Invalid option! Press Enter to go to Terminal."
        ;;
esac
