FROM jupyter/scipy-notebook

ARG openjdk_version="11"
USER root

# We will install R and packages using instructions from https://cloud.r-project.org/
# Should be installed into /usr/lib/R/site-library
RUN apt-get update -y \
    && apt-get -y upgrade \
    && apt-get -y dist-upgrade \
    && apt-get install -y --no-install-recommends "openjdk-${openjdk_version}-jdk-headless" ca-certificates-java \
    software-properties-common dirmngr build-essential curl libssl-dev libcurl4-openssl-dev libgdal-dev libre2-dev \
    apt-utils libudunits2-dev cmake lsb-release gpg-agent \
    # add the signing key (by Michael Rutter) for these repos
    # To verify key, run gpg --show-keys /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc
    # Fingerprint: 298A3A825C0D65DFD57CBB651716619E084DAB9
    && wget -qO- https://cloud.r-project.org/bin/linux/ubuntu/marutter_pubkey.asc \
    | sudo tee -a /etc/apt/trusted.gpg.d/cran_ubuntu_key.asc \
    # add the R 4.0 repo from CRAN -- adjust 'focal' to 'groovy' or 'bionic' as needed
    && add-apt-repository -y "deb https://cloud.r-project.org/bin/linux/ubuntu $(lsb_release -cs)-cran40/" \
    && gpg-agent --daemon \
    # Get access to 5000+ CRAN Packages
    && add-apt-repository -y ppa:c2d4u.team/c2d4u4.0+ \
    && apt autoremove -y \
    && apt-get -y clean all \
    && rm -rf /var/lib/apt/lists/*

ENV R_HOME /usr/lib/R
ENV R_LIBS_USER /usr/lib/R/library
# https://cran.r-project.org/web/packages/arrow/vignettes/install.html
ENV NOT_CRAN true
ENV ARROW_GCS=ON

COPY r-packages.txt /tmp/r-packages.txt

RUN apt update && \
    # vim support
    apt-get -y install vim && \
    # required for json parsing using bash
    apt-get -y install jq && \
    # used to find and kill files user have open
    apt-get -y install lsof && \
    # installing texlive-full
    apt-get -y install texlive-full && \
    # Installing bsdmainutils, helped solve colrm message after every command in the terminal
    apt-get install -y bsdmainutils && \
    xargs apt-get install -y --no-install-recommends < /tmp/r-packages.txt && \
    apt autoremove -y && \
    apt-get -y clean all && \
    rm -rf /var/lib/apt/lists/*

COPY jwsacruncher-2.2.4.zip /tmp/jwsacruncher-2.2.4.zip

# Setup R java support and install R packages that are not available as Ubuntu packages
RUN R CMD javareconf -e && \
    R -e "install.packages('RTextTools', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('configr', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('SSBtools', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('RegSDC', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('oysteR', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('writexl', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('concaveman', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('cppRouting', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('rjwsacruncher', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('klassR', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('antiword', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('textshape', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('striprtf', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('textreadr', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('terra', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('raster', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('leaflet', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('languageserver', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('sotkanet', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('ggiraph', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('dcmodify', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('simputation', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "library(rio); install_formats()" && \
    R -e "install.packages('arrow', dependencies=FALSE, repos='https://cloud.r-project.org/')" && \
    R -e "remotes::install_github('r-barnes/dggridR', vignette=TRUE)" && \
    R -e "remotes::install_github('statisticsnorway/Kostra')" && \
    R -e "remotes::install_github('statisticsnorway/SdcForetakPerson')" && \
    R -e "install.packages('dotenv', dependencies=FALSE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('PriceIndices', dependencies=TRUE, repos='http://cran.rstudio.com/')" && \
    R -e "install.packages('sfarrow', dependencies=FALSE, repos='https://cloud.r-project.org/')" && \
    rm -rf /tmp/downloaded_packages/ /tmp/*.rds && \
    # Doesn t work with Java11 - use a custom one
    #curl --silent -L -o- https://github.com/jdemetra/jwsacruncher/releases/download/v2.2.3/jwsacruncher-2.2.3-bin.zip | bsdtar -xvf- -C /opt && \
    unzip /tmp/jwsacruncher-2.2.4.zip -d /opt && fix-permissions /opt/jwsacruncher-2.2.4 && rm -f /tmp/jwsacruncher-2.2.4.zip && \
    # Create a symlink at /usr/bin so users can call jwsacruncher from anywhere
    ln -s /opt/jwsacruncher-2.2.4/bin/jwsacruncher /usr/bin/jwsacruncher

USER $NB_UID

RUN echo "**** install jupyterlab-git ****" && \
    python3 -m pip install --upgrade jupyterlab-git && \
    echo "**** install nbdime ****" && \
    python3 -m pip install --upgrade nbdime && \
    jupyter labextension install --no-build nbdime-jupyterlab && \
    echo "**** install nbstripout ****" && \
    python3 -m pip install nbstripout && \
    echo "**** install papermill ****" && \
    python3 -m pip install papermill && \
    echo "**** install ipywidgets ****" && \
    python3 -m pip install ipywidgets && \
    echo "**** install jupyter_server_proxy ****" && \
    python3 -m pip install jupyter-server-proxy && \
    echo "**** install holoviz panel ****" && \
    python3 -m pip install pyviz_comms && \
    python3 -m pip install panel==0.13.1rc2 && \
    jupyter serverextension enable panel.io.jupyter_server_extension && \
    echo "**** install Voilà ****" && \
    python3 -m pip install voila && \
    echo "**** install Plotly ****" && \
    # JupyterLab renderer support
    python3 -m pip install plotly && \
    echo "**** install geopandas ****" && \
    python3 -m pip install geopandas && \
    echo "**** install ipyleaflet ****" && \
    python3 -m pip install ipyleaflet && \
    echo "**** install descartes ****" && \
    python3 -m pip install descartes && \
    echo "**** install dash ****" && \
    python3 -m pip install jupyter-dash && \
    #echo "**** install streamlit ****" && \
    #showstopper: https://github.com/streamlit/streamlit/issues/2703
    #python3 -m pip install streamlit && \
    echo "**** install jupyter-lsp ****" && \
    python3 -m pip install jupyterlab-lsp && \
    python3 -m pip install python-language-server[all] && \
    echo "**** install ipysheet ****" && \
    python3 -m pip install ipysheet && \
    echo "**** install ipyaggrid ****" && \
    python3 -m pip install ipyaggrid && \
    #echo "**** install qgrid ****" && \
    #showstopper: https://github.com/quantopian/qgrid/issues/350
    #python3 -m pip install qgrid2 && \
    echo "**** install fuzzywuzzy[speedup] ****" && \
    python3 -m pip install fuzzywuzzy[speedup] && \
    echo "**** install jupyterlab-system-monitor ****" && \
    python3 -m pip install jupyterlab-system-monitor && \
    echo "**** install jupytext ****" && \
    python3 -m pip install jupytext && \
    #echo "**** install lckr-jupyterlab-variableinspector ****" && \
    #showstopper: https://github.com/lckr/jupyterlab-variableInspector/issues/122
    #python3 -m pip install --upgrade lckr-jupyterlab-variableinspector && \
    echo "**** uninstall IPython Parallels (comes default with dockerhub image)  ****" && \
    python3 -m pip uninstall -y ipyparallel && \
    # pipenv is used for keeping track of and loading the specific package dependencies of each repository
    # Together with with envkernel Jupyter users can create Jupyter kernels with a different environment.
    echo "**** install pipenv envkernel ****" && \
    python3 -m pip install pipenv envkernel && \
    echo "**** install poetry ****" && \
    python3 -m pip install poetry && \
    echo "**** install collapsible headers (for Jupyterlab >= 3.0) ****" && \
    python3 -m pip install aquirdturtle_collapsible_headings && \
    echo "**** install sphinx ****" && \
    python3 -m pip install sphinx sphinx-autodoc-defaultargs sphinx-autodoc-typehints sphinx-rtd-theme && \
    echo "**** disable extensions which allow downloading ****" && \
    jupyter labextension disable @jupyterlab/docmanager-extension:download && \
    jupyter labextension disable @jupyterlab/filebrowser-extension:download && \
    echo "**** clean caches and finish up ****" && \
    python3 -m pip cache purge && \
    conda clean --all -y && \
    jupyter lab clean && \
    jupyter lab build --dev-build=False && \
    python3 -m pip install --upgrade jupyterhub && \
    jupyterhub upgrade-db

RUN echo "**** install common pip packages ****" && \
    python3 -m pip install pytest pytest_tornasync pytest-cov pytest-mock  && \
    python3 -m pip install pyjstat xmltodict lxml holidays PyGithub pre-commit pyminizip rich openpyxl pyarrow==9.0.* python-dotenv poetry && \
    python3 -m pip install ssb-datadoc && \
    python3 -m pip install ssb-project-cli && \
    python3 -m pip cache purge

#Disable Jupyter extension manager
RUN jupyter labextension disable @jupyterlab/extensionmanager-extension

USER root

# Python vuln check, and remove package afterwards
RUN pip install safety
RUN safety check --full-report -i 49913 -i 50463 -i 50664
RUN pip uninstall -y safety && \
    rm -rf /home/jovyan/.cache

# Set localtime to Europe/Oslo
RUN rm -f /etc/localtime && \
    ln -s /usr/share/zoneinfo/Europe/Oslo /etc/localtime

# Installing quarto https://quarto.org/
# not installing .deb file because some features don't work
RUN wget https://github.com/quarto-dev/quarto-cli/releases/download/v1.0.38/quarto-1.0.38-linux-amd64.tar.gz -P /tmp/ && \
    tar -zxf /tmp/quarto-1.0.38-linux-amd64.tar.gz -C /usr/local/ && \
    ln -s /usr/local/quarto-1.0.38/bin/quarto /usr/local/bin/quarto && \
    quarto install --no-prompt extension quarto-ext/fontawesome && \
    rm -rf /tmp/quarto-1.0.38-linux-amd64.tar.gz

# adding a custom bashrc with git branch in PS1
COPY common-bashrc /etc/skel/.bashrc

# Install ssb-gitconfig.py script
RUN wget -O /usr/local/bin/ssb-gitconfig.py https://raw.githubusercontent.com/statisticsnorway/kvakk-git-tools/main/ssb-gitconfig/ssb-gitconfig.py
RUN chmod +x /usr/local/bin/ssb-gitconfig.py

COPY check-git-config.bash /usr/local/bin/check-git-config.sh
RUN chmod +x /usr/local/bin/check-git-config.sh

COPY jupyter_notebook_extra_config.py /tmp/
RUN cat /tmp/jupyter_notebook_extra_config.py >> /etc/jupyter/jupyter_notebook_config.py && \
    chmod g-w /etc/jupyter/*.py && \
    rm -f /tmp/jupyter_notebook_extra_config.py

#Prevent installation of extentions, by removing write privilege in extension folders.
RUN chmod u-w  /opt/conda/share/jupyter/labextensions
RUN chmod u-w  /opt/conda/share/jupyter/nbextensions
RUN chmod u-w  /opt/conda/share/jupyter/lab/extensions

USER $NB_UID
