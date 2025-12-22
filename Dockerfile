# Odoo 19.0 Docker Image
FROM python:3.12-slim-bookworm

LABEL maintainer="brave"
LABEL version="19.0"
LABEL description="Odoo 19.0 ERP System"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive \
    ODOO_VERSION=19.0 \
    ODOO_RC=/etc/odoo/odoo.conf

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Core dependencies
    ca-certificates \
    curl \
    dirmngr \
    gnupg \
    libpq-dev \
    libsasl2-dev \
    libldap2-dev \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
    libfreetype6-dev \
    liblcms2-dev \
    zlib1g-dev \
    # Database clients
    postgresql-client \
    # Tools
    git \
    wget \
    xz-utils \
    # Node.js for assets
    nodejs \
    npm \
    # Fonts
    fonts-liberation \
    fonts-noto-cjk \
    # wkhtmltopdf dependencies
    fontconfig \
    libjpeg62-turbo \
    libx11-6 \
    libxcb1 \
    libxext6 \
    libxrender1 \
    xfonts-75dpi \
    xfonts-base \
    && rm -rf /var/lib/apt/lists/*

# Install wkhtmltopdf 0.12.6 (with patched Qt for headers/footers)
RUN wget -q https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && apt-get update \
    && apt-get install -y --no-install-recommends ./wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && rm -f wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

# Create odoo user
RUN useradd -ms /bin/bash -u 1000 odoo

# Set working directory
WORKDIR /opt/odoo

# Copy application files
COPY --chown=odoo:odoo . /opt/odoo/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Install additional Python packages if needed
RUN pip install --no-cache-dir \
    psycopg2-binary \
    gevent

# Create necessary directories
RUN mkdir -p /var/lib/odoo \
    /etc/odoo \
    /var/log/odoo \
    && chown -R odoo:odoo /var/lib/odoo /etc/odoo /var/log/odoo

# Copy configuration file
COPY --chown=odoo:odoo docker/odoo.conf /etc/odoo/odoo.conf

# Expose Odoo services
EXPOSE 8069 8071 8072

# Switch to odoo user
USER odoo

# Set volumes
VOLUME ["/var/lib/odoo", "/var/log/odoo"]

# Default command
ENTRYPOINT ["/opt/odoo/odoo-bin"]
CMD ["-c", "/etc/odoo/odoo.conf"]
