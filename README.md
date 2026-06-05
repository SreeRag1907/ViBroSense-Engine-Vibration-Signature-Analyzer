%------------------------------------------------------------------
%  C SREERAG  –  Résumé  (Data Analytics / ML Focus)
%------------------------------------------------------------------
\documentclass[10pt,letterpaper]{article}

\usepackage[top=0.45in,bottom=0.45in,left=0.55in,right=0.55in]{geometry}
\usepackage{enumitem}
\usepackage{fontawesome}
\usepackage{titlesec}
\usepackage[hidelinks]{hyperref}
\usepackage{xcolor}
\usepackage{tabularx}
\usepackage[T1]{fontenc}
\usepackage{microtype}

\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\tabcolsep}{0pt}

\definecolor{accent}{RGB}{24,72,150}

\titleformat{\section}{\large\bfseries\color{accent}}{}{0em}{}
  [\color{accent}\titlerule\vspace{1pt}]
\titlespacing{\section}{0pt}{6pt}{3pt}

%-- helpers
\newcommand{\proj}[3]{%
  \vspace{1pt}%
  \begin{tabular*}{\textwidth}{@{}l@{\extracolsep{\fill}}r@{}}
    \textbf{#1} & \small #3\\
    \multicolumn{2}{@{}l@{}}{\small\textit{#2}}\\
  \end{tabular*}\vspace{0.5pt}}

\newcommand{\edu}[4]{%
  \vspace{1pt}%
  \begin{tabular*}{\textwidth}{@{}l@{\extracolsep{\fill}}r@{}}
    \textbf{#1} & \small\textit{#4}\\
    \small\textit{#2} & \small #3\\
  \end{tabular*}\vspace{0.5pt}}

\newlist{bullets}{itemize}{1}
\setlist[bullets]{
  label=\small$\bullet$,
  leftmargin=14pt,
  itemsep=0.5pt,
  topsep=1pt,
  parsep=0pt,
  partopsep=0pt
}

%==================================================================
\begin{document}
%==================================================================

%-- HEADER
\begin{center}
  {\LARGE\bfseries C\ SREERAG}\\[4pt]
  \small
  \faPhone\ +91\,7083919479\enspace\textbar\enspace
  \faEnvelope\ \href{mailto:c.sreerag17@gmail.com}{c.sreerag17@gmail.com}\enspace\textbar\enspace
  \faMapMarker\ Pune, Maharashtra\\[3pt]
  \faLinkedin\ \href{https://linkedin.com/in/c-sreerag}{linkedin.com/in/c-sreerag}\enspace\textbar\enspace
  \faGithub\ \href{https://github.com/c-sreerag}{github.com/c-sreerag}\enspace\textbar\enspace
  \faGlobe\ Portfolio
\end{center}

%-- SUMMARY
\section{Professional Summary}
MCA student (CGPA 8.73) with a strong foundation in \textbf{Python-based data analytics,
machine learning, and signal processing}. Independently built two end-to-end analytical
systems --- a multivariate time-series anomaly-detection engine for diesel emissions
(DieselSense) and an FFT-based vibration fault-diagnosis tool (ViBroSense) --- directly
aligned with industrial condition monitoring. Awarded \textbf{2nd place at Pragyantra 2026
National AI Hackathon} (100+ teams) for an AI-powered analytics product. Proficient in
Python ML pipelines, time-series feature engineering, and automated threshold alerting;
eager to apply these skills in a real-world engineering environment.

%-- SKILLS
\section{Technical Skills}

\begin{tabular*}{\textwidth}{@{}p{2.4cm} l@{}}
  \textbf{Languages}    & Python (Pandas, NumPy, SciPy, Scikit-learn), SQL\\[2pt]
  \textbf{ML / Stats}   & Isolation Forest, Random Forest, ARIMA, FFT, Hilbert Transform,
                          Spectral Kurtosis, PCA\\[2pt]
  \textbf{Analytics}    & Time-Series Analysis, Anomaly Detection, Predictive Modelling,
                          Feature Engineering, Threshold Alerting\\[2pt]
  \textbf{Viz / Tools}  & Matplotlib, Seaborn, Jupyter Notebook, FastAPI, Git, Agile/Scrum\\[2pt]
  \textbf{Data/APIs}    & Supabase (PostgreSQL), OpenAI API, REST APIs\\
\end{tabular*}

%-- PROJECTS
\section{Projects}

%-- Project 1
\proj
  {DieselSense\ ---\ Diesel Engine Emission Analytics \& Condition Monitoring}
  {Python $\cdot$ Pandas $\cdot$ NumPy $\cdot$ Scikit-learn $\cdot$ Matplotlib $\cdot$ Seaborn $\cdot$ FastAPI}
  {GitHub}
\begin{bullets}
  \item Built an end-to-end \textbf{time-series analytics pipeline} over 720 hours of
        8-channel diesel engine sensor data (RPM, temperature, boost pressure, NOx, PM,
        fuel rate, exhaust back-pressure, coolant temperature).
  \item Applied \textbf{Isolation Forest} (unsupervised; no labelled data required) with
        multivariate lag and rolling-statistics features, achieving \textbf{100\% recall}
        on injected failure events across all six fault types.
  \item Trained a \textbf{Random Forest classifier} for fault categorisation
        (F1\,=\,1.0 on test set); identified temperature and NOx lag-24h as top predictors
        via feature-importance analysis.
  \item Tracked \textbf{NOx and PM emissions against EU Stage V limits}, generating
        automated threshold-breach alerts --- directly replicating the emission-reduction
        monitoring workflow for high-power diesel engines.
  \item Computed a rolling \textbf{Degradation Index} (0--100) combining emission index,
        thermal efficiency ratio, and anomaly density as a composite early-warning health score.
  \item Automated the full pipeline --- feature engineering, model training, alert
        generation, and chart export --- with a FastAPI backend for real-time deployment.
\end{bullets}

%-- Project 2
\proj
  {ViBroSense\ ---\ Engine Vibration Signature Analyzer \& Fault Detector}
  {Python $\cdot$ SciPy (FFT, Hilbert) $\cdot$ NumPy $\cdot$ Matplotlib $\cdot$ Signal Processing}
  {GitHub}
\begin{bullets}
  \item Synthesised four realistic engine fault conditions (healthy, cylinder misfire,
        worn bearing, structural resonance) from \textbf{first-principles physics} ---
        real firing frequencies, SKF 6205 bearing geometry, and torsional resonance modes.
  \item Implemented the \textbf{full vibration analysis pipeline} equivalent to MATLAB:
        FFT decomposition \textrightarrow{} Hilbert envelope \textrightarrow{}
        Spectral Kurtosis \textrightarrow{} automatic fault-signature matching.
  \item Detected misfire at 0.5$\times$ firing frequency (25\,Hz), bearing outer-race
        fault (BPFO) at 107.6\,Hz, and structural resonance at 420\,Hz --- all
        correctly classified with zero false positives.
  \item Produced publication-quality spectral plots (FFT, envelope spectrum, kurtogram)
        for each fault condition, mirroring the diagnostic workflow used in industrial
        condition monitoring of MTU / Rolls-Royce diesel engines.
\end{bullets}

%-- Project 3
\proj
  {SpendLens\ ---\ AI-Powered Financial Analytics Platform}
  {Python $\cdot$ OpenAI API (GPT-4o-mini) $\cdot$ Supabase (PostgreSQL) $\cdot$ React Native}
  {\textbf{2nd Place} --- Pragyantra 2026 National AI Hackathon (100+ Teams)}
\begin{bullets}
  \item Built a mobile analytics application that parses raw bank SMS text, uses
        \textbf{GPT-4o-mini} to auto-classify transactions, and surfaces spending
        patterns over time-series financial data.
  \item Designed dashboards for budget monitoring, subscription detection, and
        real-time financial insights; integrated OpenAI APIs with PostgreSQL for
        secure data pipelines and AI-powered analytics.
\end{bullets}

%-- EDUCATION
\section{Education}

\edu
  {Master of Computer Applications (MCA)}
  {PES Modern College of Engineering, Pune}
  {CGPA: 8.73\,/\,10}
  {2024 -- 2026 (Expected)}

\edu
  {Bachelor of Computer Applications (BCA)}
  {Dr.\ D.Y.\ Patil ACS College, Pune}
  {CGPA: 9.08\,/\,10}
  {2021 -- 2024}

%-- ACHIEVEMENTS
\section{Achievements}
\begin{bullets}
  \item \textbf{2nd Place} --- Pragyantra 2026 National AI Hackathon;
        developed SpendLens (AI-powered analytics) against 100+ teams nationwide.
  \item \textbf{1st Place} --- Navonmesh 2025 State-Level Project Competition;
        IoT-based Smart Fluid Monitoring System (real-time sensor analytics).
  \item \textbf{Elite + Gold (Top 1\%)} --- NPTEL Edge Computing by IIT Kanpur;
        scored 93\% among 2,261+ learners.
\end{bullets}

\end{document}
