## 리눅스 가상 머신에 VS Code 설치, GitHub 연동 및 TensorFlow 설치 가이드

이 가이드는 리눅스 가상 머신(Ubuntu 기준)에 VS Code를 설치하고, GitHub와 SSH로 연동하며, TensorFlow를 위한 파이썬 가상 환경을 구축하는 방법을 안내합니다.

-----

### 1\. VS Code 설치

공식 웹사이트에서 VS Code 설치 파일을 다운로드합니다. Ubuntu를 사용하고 있으므로 **`.deb`** 파일을 선택합니다.
<img width="842" height="601" alt="vscode설치" src="https://github.com/user-attachments/assets/39af1315-c5f7-4cfd-87e7-be9d0053d94b" />

터미널에서 다운로드한 `.deb` 파일을 사용하여 VS Code를 설치합니다.

```bash
sudo dpkg -i code_1.103.0-1754517494_amd64.deb
```

-----

### 2\. GitHub SSH 연동

GitHub와 안전하게 통신하기 위해 SSH 키를 생성하고 등록합니다.

#### **SSH 키 파일 디렉토리 생성 및 권한 설정**

먼저, SSH 키를 저장할 디렉토리를 만들고 권한을 설정합니다.

```bash
mkdir ~/.ssh
chmod 700 ~/.ssh
```

#### **새로운 SSH 키 생성**

GitHub 계정에 등록할 새로운 SSH 키를 생성합니다. "your\_email@example.com" 부분은 본인의 GitHub 이메일 주소로 변경하세요.

```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

#### **`.ssh` 키 파일 권한 변경**

생성된 키 파일의 권한을 올바르게 설정합니다.

```bash
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
```

#### **GitHub에 SSH 연결 설정 확인**

GitHub에 SSH 키가 제대로 등록되었는지 확인합니다.

```bash
ssh -T git@github.com
```

#### **`known_hosts` 파일 권한 설정**

`known_hosts` 파일의 권한을 변경하여 보안을 강화합니다.

```bash
chmod 600 ~/.ssh/known_hosts
```

-----

### 3\. TensorFlow 가상 환경 설치

프로젝트의 의존성을 관리하기 위해 파이썬 가상 환경을 생성합니다.

#### **프로젝트 디렉토리 생성**

`opencv_tf` 디렉토리를 생성하고 이동합니다.

```bash
cd ~
mkdir opencv_tf
cd opencv_tf/
```

#### **파이썬 가상 환경 생성 및 활성화**

`venv` 모듈을 설치하고 `tfvenv`라는 가상 환경을 생성한 후, 활성화합니다.

```bash
sudo apt install python3.10-venv
python3 -m venv tfvenv
source tfvenv/bin/activate
```

#### **파이썬 가상 환경에 TensorFlow 설치**

가상 환경이 활성화된 상태에서 TensorFlow를 설치합니다.

```bash
pip install tensorflow
```

-----

### 4\. 가상 머신 용량 확장 (용량이 부족할 경우)

TensorFlow 설치 중 용량이 부족할 경우, 가상 머신의 하드디스크 용량을 늘려야 합니다.

#### **가상 머신 하드디스크 용량 재설정**
<img width="653" height="599" alt="가상환경 용량늘리기_1" src="https://github.com/user-attachments/assets/fa7cfd64-0560-47d6-a5da-c2715cfe0365" />

1.  가상 머신을 **종료**한 후, VMware 메뉴에서 \*\*`VM` \> `Settings...`\*\*로 이동합니다.

<img width="759" height="738" alt="가상환경용량늘리기_2" src="https://github.com/user-attachments/assets/65d9e161-6f6b-4d93-894f-7232a0ff7c66" />

2.  `Hard Disk (SCSI)`를 선택하고, `Expand...` 버튼을 클릭합니다.
3.  `Maximum disk size (GB)`를 원하는 용량으로 설정하고 `Expand`를 클릭합니다.

#### **가상 머신 파티션 재설정**

1.  우분투 내에서 파티션 도구인 `gparted`를 설치합니다.

    ```bash
    sudo apt-get install gparted
    ```

2.  터미널에서 `gparted`를 실행합니다.

    ```bash
    sudo gparted
    ```

<img width="781" height="622" alt="가상환경 용량늘리기_3" src="https://github.com/user-attachments/assets/3ad5de17-8544-4b27-acec-fcc839301b39" />

3.  파티션 목록에서 용량을 확장할 파티션(보통 `/`가 마운트된 파티션)을 우클릭하고 \*\*`Resize/Move`\*\*를 선택합니다.

<img width="776" height="534" alt="가상환경용량늘리기_4" src="https://github.com/user-attachments/assets/40836c35-4c75-4de2-8612-1d3b369b6459" />

4.  \*\*`New size`\*\*를 최대로 설정하고 `Resize`를 클릭한 뒤, 상단의 **초록색 체크표시**를 눌러 변경사항을 적용합니다.

-----

### 5\. GitHub Repository 연동

로컬 디렉토리를 Git 저장소로 초기화하고 GitHub와 연동합니다.

#### **저장소 생성 및 Git 초기화**

프로젝트 디렉토리인 `opencv_tf` 안에 `11_opencv` 디렉토리를 만들고, Git 저장소로 초기화합니다.

```bash
mkdir 11_opencv
cd 11_opencv/
git init
git branch -m master main
```
