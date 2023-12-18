FROM ubuntu:20.04

ENV PROGRAMS_ROOT_PATH /opt
ENV DOWNLOAD_DIR /tmp
ENV ANDROID_SDK_VERSION 10406996
ENV ANDROID_CMDLINE_VERSION 11
ENV ANDROID_SDK_ROOT ${PROGRAMS_ROOT_PATH}/android-sdk
ENV FLUTTER_VERSION 3.10.6
ENV FLUTTER_ROOT /opt/flutter
ENV GRADLE_VERSION 7.4.2
ENV GRADLE_HOME ${PROGRAMS_ROOT_PATH}/gradle
ENV KOTLIN_VERSION 1.9.10
ENV TZ="America/Sao_Paulo"
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

RUN \
  apt-get update \
  && apt-get install -yq tzdata \
  && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
  && dpkg-reconfigure -f noninteractive tzdata

RUN \
  mkdir -p ${ANDROID_SDK_ROOT}/cmdline-tools \
  && mkdir -p ${FLUTTER_ROOT} \
  && apt update \
  && apt install wget git curl zip unzip xz-utils pkg-config libglu1-mesa ninja-build cmake clang libgtk-3-dev openjdk-17-jdk-headless ruby ruby-dev -y \
  && wget -O ${DOWNLOAD_DIR}/commandlinetools-linux-${ANDROID_SDK_VERSION}_latest.zip https://dl.google.com/android/repository/commandlinetools-linux-${ANDROID_SDK_VERSION}_latest.zip \
  && wget -O ${DOWNLOAD_DIR}/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz \
  && wget -O ${DOWNLOAD_DIR}/gradle-${GRADLE_VERSION}-bin.zip https://services.gradle.org/distributions/gradle-${GRADLE_VERSION}-bin.zip \
  && wget -O ${DOWNLOAD_DIR}/kotlin-compiler-${KOTLIN_VERSION}.zip https://github.com/JetBrains/kotlin/releases/download/v${KOTLIN_VERSION}/kotlin-compiler-${KOTLIN_VERSION}.zip \
  && unzip ${DOWNLOAD_DIR}/*tools*linux*.zip -d ${ANDROID_SDK_ROOT}/cmdline-tools \
  && mv ${ANDROID_SDK_ROOT}/cmdline-tools/cmdline-tools ${ANDROID_SDK_ROOT}/cmdline-tools/${ANDROID_CMDLINE_VERSION} \
  && tar -xf ${DOWNLOAD_DIR}/flutter_linux_${FLUTTER_VERSION}-stable.tar.xz -C ${PROGRAMS_ROOT_PATH} \
  && unzip ${DOWNLOAD_DIR}/gradle-${GRADLE_VERSION}-bin.zip -d ${GRADLE_HOME} \
  && unzip ${DOWNLOAD_DIR}/kotlin-compiler-${KOTLIN_VERSION}.zip -d ${PROGRAMS_ROOT_PATH} \
  && mv /opt/kotlinc /opt/kotlin \
  && rm -rf ${DOWNLOAD_DIR}/* \
  && chown -R root:root /opt/* \
  && gem install fastlane \
  && apt auto-clean

ENV GRADLE_HOME /opt/gradle/gradle-${GRADLE_VERSION}
ENV PATH "$PATH:/opt/android-sdk/cmdline-tools/${ANDROID_CMDLINE_VERSION}/bin:${ANDROID_SDK_ROOT}/build-tools:${ANDROID_SDK_ROOT}/cmdline-tools:${ANDROID_SDK_ROOT}/platform-tools:${GRADLE_HOME}/bin"
ENV PATH "/opt/flutter/bin:$PATH"
ENV PATH "/opt/kotlin/bin:$PATH"

RUN \
  yes | sdkmanager --licenses \
  && sdkmanager --install "build-tools;30.0.3" \
  && sdkmanager --install "platforms;android-33" \
  && sdkmanager --install platform-tools

# Tem que aparecer na branch master