FROM ubuntu:latest

# 必要なパッケージのインストール
RUN apt-get update && \
    apt-get install -y openssh-server sudo && \
    mkdir /var/run/sshd

# SSH用の設定
RUN echo 'root:YOUR_PASSWORD' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

# SSHがルートユーザーでのログインを許可することに注意
# 本番環境ではセキュリティのために別のユーザーを作成することを推奨

# ポート22を公開
EXPOSE 22

# SSHサービスの起動
CMD ["/usr/sbin/sshd", "-D"]
