\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{layout/tudelft-report}[18-11-2022 v1.0 TU Delft C&S MSc Report Class]
\LoadClass[10pt, oneside]{book}

%% Main packages in the document
\RequirePackage{amsmath}                % Mathematics
\RequirePackage{amssymb}                % Symbols
\RequirePackage{amsfonts}               % Fonts
\RequirePackage[table]{xcolor}          % Using colours in documents
\RequirePackage{tabularx}               % Additional functions to tables
\RequirePackage{booktabs}               % Adds more line functionality to tables
\RequirePackage{epigraph}               % Allow comments on the Part page
\RequirePackage{multirow}               % Counterpart of multi columns
\RequirePackage{enumitem}               % Customise the list spacing
\RequirePackage{geometry}               % Document geometry
\RequirePackage{titlesec}               % Custom titles
\RequirePackage{titletoc}               % Custom table of contents
\RequirePackage{fancyhdr}               % Custom header/footer
\RequirePackage{graphicx}               % Adding images
\RequirePackage{float}                  % Additional float parameters
\RequirePackage{tikz}                   % Create graphic elements
\RequirePackage{datetime}               % Used in preface for monthname
\RequirePackage[final]{microtype}       % Refinements towards typographical perfection
\RequirePackage[nottoc]{tocbibind}      % Add the lists to the table of contents
\RequirePackage{xspace}                 % Ensures correct spacing after macros like \deg
\RequirePackage{etoolbox}               % General toolbox (e.g. \ifdefvoid)
\RequirePackage{pdfpages}               % Insert pdfs                    
\RequirePackage{afterpage}              % Commands after pagebreak
\RequirePackage{mathtools}              % Extension to amsmath
\RequirePackage{mathdots}               % Adds vdots, iddots, etc
\RequirePackage{wrapfig}                % Wrap figures around text
\RequirePackage{pifont}                 % Extra symbols
\RequirePackage{nomencl}                % Nomenclature
\RequirePackage{neuralnetwork}          % Neural Networks.
\RequirePackage{physics}                % Physics symbols like grad, 
\RequirePackage{booktabs}               % Pretty and simple tables
\RequirePackage{colortbl}               % Coloring tables
\RequirePackage{xspace}
\RequirePackage{bm}
\RequirePackage{bbm}
\RequirePackage{multicol}
\RequirePackage{tkz-euclide}
\RequirePackage{subfig}
\RequirePackage{pgfplots}
\RequirePackage{mathrsfs}
\RequirePackage{svg}
\RequirePackage{bigfoot}
\RequirePackage{fontspec}               % Custom fonts
\usepackage{longtable}

% Packages with options
\RequirePackage[labelfont=bf,justification=centering]{caption}
\RequirePackage[hidelinks]{hyperref}    % Improved referencing/links
\RequirePackage[capitalise]{cleveref}
\RequirePackage[ruled]{algorithm2e}
\RequirePackage[sorting=none, maxbibnames=1, isbn=false]{biblatex}

\pgfplotsset{compat=newest}

% Load the tikz libraries
\usetikzlibrary{
    calc,
    shapes.misc,
    shapes.geometric,
    arrows, 
    arrows.meta, 
    fit, 
    positioning, 
    shapes.symbols, 
    chains, 
    mindmap,
    decorations.pathmorphing,
    decorations.markings,
    patterns,
    backgrounds,
    intersections,  
}

%% Set up page geometry and margins
\geometry{
    a4paper,
    hscale=0.77,
    vscale=0.8
}

% Colors and tikz styles
\input{styling.tex}

%% Define the title, author, etc
\renewcommand{\title}[1]{%
    \def\@title{#1}%
    \hypersetup{pdftitle=#1}} % Adding to metadata

\renewcommand*{\author}[2][]{%
    \def\@author{#2}%
    \def\@author@short{#1}%
    \hypersetup{pdfauthor=\ifdefvoid{\@author@short}{#2}{#1}}} % Adding to metadata

\newcommand*\subtitle[1]{\def\@subtitle{#1}}
\newcommand\subject[1]{\def\@subject{#1}}

% Setting up \autoref to use uppercase
\def\sectionautorefname{Section}
\def\chapterautorefname{Chapter}
\let\subsectionautorefname\sectionautorefname
\let\subsubsectionautorefname\sectionautorefname

% __ Load fonts __
\setmainfont{Arial}
\setmathsf{Arial}
\setmathtt{Arial}
\newfontfamily\tudtitlefamily[Path=layout/tudelft/]{TUDelft-UltraLight.ttf}
\newfontfamily\quotefont{Georgia}
\def\largetitlestyle{\tudtitlefamily}
\def\titlestyle{\normalfont}
\AtBeginEnvironment{quote}{\quotefont}

% 3. Adjust Headers and TOC

% Formatting the part header and enabling epigraphs to add comments
\titleformat{\part}[display]
    {\flushright\titlestyle}
    {\fontsize{72}{72}\bfseries\largetitlestyle Part \thepart}
    {0pt}
    {\Huge\thispagestyle{epigraph}}
\titlespacing*{\part}{0pt}{0pt}{2\baselineskip}
\setlength\epigraphwidth{.7\textwidth}

% Formatting chapter titles and spacing
\titleformat{\chapter}[display]
    {\flushright}
    {\fontsize{72}{72}\selectfont\largetitlestyle\thechapter}
    {0pt}
    {\Huge\titlestyle}
\titlespacing*{\chapter}{0pt}{0pt}{2\baselineskip}

% Formatting section titles and spacing
\titleformat{\section}
    {\Large\titlestyle\bfseries}
    {\thesection.}
    {5pt}
    {}
\titlespacing*{\section}{0pt}{\baselineskip}{0pt}

% Formatting subsections titles and spacing
\titleformat{\subsection}
    {\large\titlestyle\bfseries}
    {\thesubsection.}
    {5pt}
    {}
\titlespacing*{\subsection}{0pt}{\baselineskip}{0pt}

% Formatting subsubsections titles and spacing
\titleformat{\subsubsection}
    {\titlestyle\bfseries}
    {}
    {0pt}
    {}
\titlespacing*{\subsubsection}{0pt}{\bigskipamount}{0pt}

% Changing font and spacing in the TOC
\dottedcontents{chapter}[1.5em]{\vspace{0.5\baselineskip}\titlestyle\bfseries}{1.5em}{0pc}
\dottedcontents{section}[3.8em]{\titlestyle}{2.3em}{8pt}
\dottedcontents{subsection}[7em]{\titlestyle}{3.2em}{8pt}

% Adding a head rule to pages
\renewcommand*\headrule{%
    {\hrule\@height\headrulewidth\@width\headwidth}%
    \vskip-\headrulewidth}

% Page style for title pages
\fancypagestyle{plain}{%
    \fancyhf{}
    \renewcommand*\headrulewidth{0pt}
    \fancyfoot[C]{\thepage}}

% Fancy style for the main matter, depends on oneside/twoside option
\if@twoside%
    \fancyhf{}
    \fancyhead[LE,RO]{\titlestyle\thepage}
    \fancyhead[RE]{\titlestyle\nouppercase{\leftmark}}
    \fancyhead[LO]{\titlestyle\nouppercase{\rightmark}}
    \RequirePackage{emptypage} % Clears empty pages
\else%
    \fancyhf{}
    \fancyhead[R]{\titlestyle\thepage}
    \fancyhead[L]{\titlestyle\nouppercase{\rightmark}}
\fi

\pagestyle{fancy} % Setting it to default

% ___ Cover page definition ___
\input{frontmatter/coverpage}

% ___ Nomenclature ___
\renewcommand\nomgroup[1] {
    \item[
        \bfseries
            \ifstrequal{#1}{A}{List of Abbreviations}{
            \ifstrequal{#1}{C}{Constants}{
            \ifstrequal{#1}{S}{List of Symbols}}}
    ]
}
\newcommand{\nomunit}[1]{%
\renewcommand{\nomentryend}{\hspace*{\fill}#1}}

%% Add command for a blank page:
\newcommand\blankpage{
    \null
    \thispagestyle{empty}
    \addtocounter{page}{-1}
    \newpage
}

\makeatletter
\newcommand{\customlabel}[2]{%
   \protected@write \@auxout {}{\string \newlabel {#1}{{#2}{\thepage}{#2}{#1}{}} }%
   \hypertarget{#1}{#2}
}
\makeatother

% Add command for a general design specification:
\newcommand{\DesignSpecification}[2]{
    \begin{center}
    \begin{tikzpicture}
        \node [
            draw=primary, 
            rectangle,
            rounded corners=1.5, 
            text width=0.93\textwidth, 
            minimum width=\textwidth-24pt,
            inner sep=12pt,
            line width=1.5,
            text=black,
        ] (box) {
            #2
        };
        \node [
            anchor=south west, 
            draw=primary, 
            rectangle,
            line width=1.5,
            rounded corners=1.5,
            pattern = north east lines,
            pattern color = primary!20
        ] (rq) at ([xshift=-0.494\textwidth+0.7pt, yshift=-\pgflinewidth]box.north) {\hspace*{8pt}\textbf{Functionality Specification \customlabel{rq:#1}{#1}}\hspace*{8pt}};
        
    \end{tikzpicture}
    \end{center}
}

% Add command for a design specification:
\newcommand{\PerformanceSpecification}[2]{
    \begin{center}
    \begin{tikzpicture}
        \node [
            draw=primary, 
            rectangle,
            rounded corners=1.5, 
            text width=0.93\textwidth, 
            minimum width=\textwidth-24pt,
            inner sep=12pt,
            line width=1.5,
            text=black,
        ] (box) {
            #2
        };
        \node [
            anchor=south west, 
            draw=primary, 
            rectangle,
            line width=1.5,
            rounded corners=1.5,
            pattern = north east lines,
            pattern color = primary!20
        ] (rq) at ([xshift=-0.494\textwidth+0.7pt, yshift=-\pgflinewidth]box.north) {\hspace*{8pt}\textbf{Performance Specification \customlabel{rq:#1}{#1}}\hspace*{8pt}};
        
    \end{tikzpicture}
    \end{center}
}


% Add command for a design specification:
\newcommand{\GeneralSpecification}[2]{
    \begin{center}
    \begin{tikzpicture}
        \node [
            draw=primary, 
            rectangle,
            rounded corners=1.5, 
            text width=0.93\textwidth, 
            minimum width=\textwidth-24pt,
            inner sep=12pt,
            line width=1.5,
            text=black,
        ] (box) {
            #2
        };
        \node [
            anchor=south west, 
            draw=primary, 
            rectangle,
            line width=1.5,
            rounded corners=1.5,
            pattern = north east lines,
            pattern color = primary!20
        ] (rq) at ([xshift=-0.494\textwidth+0.7pt, yshift=-\pgflinewidth]box.north) {\hspace*{8pt}\textbf{General System Specifications \customlabel{rq:#1}{#1}}\hspace*{8pt}};
        
    \end{tikzpicture}
    \end{center}
}


% Add command for a design specification:
\newcommand{\GeneralSpecEvaluation}[2]{
    \begin{center}
    \begin{tikzpicture}
        \node [
            draw=primary, 
            rectangle,
            rounded corners=1.5, 
            text width=0.93\textwidth, 
            minimum width=\textwidth-24pt,
            inner sep=12pt,
            line width=1.5,
            text=black,
        ] (box) {
            #2
        };
        \node [
            anchor=south west, 
            draw=primary, 
            rectangle,
            line width=1.5,
            rounded corners=1.5,
            pattern = north east lines,
            pattern color = primary!20
        ] (rq) at ([xshift=-0.494\textwidth+0.7pt, yshift=-\pgflinewidth]box.north) {\hspace*{8pt}\textbf{General System Specifications Evaluation \customlabel{rq:#1}{#1}}\hspace*{8pt}};
        
    \end{tikzpicture}
    \end{center}
}

% Add command for a design specification:
\newcommand{\FuncSpecEvaluation}[2]{
    \begin{center}
    \begin{tikzpicture}
        \node [
            draw=primary, 
            rectangle,
            rounded corners=1.5, 
            text width=0.93\textwidth, 
            minimum width=\textwidth-24pt,
            inner sep=12pt,
            line width=1.5,
            text=black,
        ] (box) {
            #2
        };
        \node [
            anchor=south west, 
            draw=primary, 
            rectangle,
            line width=1.5,
            rounded corners=1.5,
            pattern = north east lines,
            pattern color = primary!20
        ] (rq) at ([xshift=-0.494\textwidth+0.7pt, yshift=-\pgflinewidth]box.north) {\hspace*{8pt}\textbf{Functionality Specifications Evaluation \customlabel{rq:#1}{#1}}\hspace*{8pt}};
        
    \end{tikzpicture}
    \end{center}
}

% Add command for a design specification:
\newcommand{\PerformSpecEvaluation}[2]{
    \begin{center}
    \begin{tikzpicture}
        \node [
            draw=primary, 
            rectangle,
            rounded corners=1.5, 
            text width=0.93\textwidth, 
            minimum width=\textwidth-24pt,
            inner sep=12pt,
            line width=1.5,
            text=black,
        ] (box) {
            #2
        };
        \node [
            anchor=south west, 
            draw=primary, 
            rectangle,
            line width=1.5,
            rounded corners=1.5,
            pattern = north east lines,
            pattern color = primary!20
        ] (rq) at ([xshift=-0.494\textwidth+0.7pt, yshift=-\pgflinewidth]box.north) {\hspace*{8pt}\textbf{Performance Specifications Evaluation \customlabel{rq:#1}{#1}}\hspace*{8pt}};
        
    \end{tikzpicture}
    \end{center}
}




% Restating the research question doesn't define a new label:
\newcommand{\RestateResearchQuestion}[2]{
    \begin{center}
    \begin{tikzpicture}
        \node [
            draw=primary, 
            rectangle,
            rounded corners=1.5, 
            text width=0.93\textwidth, 
            minimum width=\textwidth-24pt,
            inner sep=12pt,
            line width=1.5,
            text=black,
        ] (box) {
            #2
        };
        \node [
            anchor=south west, 
            draw=primary, 
            rectangle,
            line width=1.5,
            rounded corners=1.5,
            pattern = north east lines,
            pattern color = primary!20
        ] (rq) at ([xshift=-0.494\textwidth+0.7pt, yshift=-\pgflinewidth]box.north) {\hspace*{8pt}\textbf{Research Question #1}\hspace*{8pt}};
        
    \end{tikzpicture}
    \end{center}
}

% Add command for a research objective:
\newcommand{\ResearchObjective}[1]{
    \begin{center}
    \begin{tikzpicture}
        \node [
            draw=primary, 
            rectangle,
            rounded corners=1.5, 
            text width=0.93\textwidth, 
            minimum width=\textwidth-24pt,
            inner sep=12pt,
            line width=1.5,
            text=black,
        ] (box) {
            #1
        };
        \node [
            anchor=south west, 
            draw=primary, 
            rectangle,
            line width=1.5,
            rounded corners=1.5,
            pattern = north east lines,
            pattern color = primary!20
        ] (rq) at ([xshift=-0.494\textwidth+0.7pt, yshift=-\pgflinewidth]box.north) {\hspace*{8pt}\textbf{Research Objective}\hspace*{8pt}};
        
    \end{tikzpicture}
    \end{center}
}

% Physics package needs this renewcommand
\AtBeginDocument{\RenewCommandCopy\qty\SI}

% Make subsections and algorithms work with cref:
\crefname{subsection}{Subsection}{Subsections}
\crefname{algocf}{Algorithm}{Algorithms}

% __ Minor adjustments ___ 

% Array stretch
\makeatletter
\renewcommand*\env@matrix[1][\arraystretch]{%
  \edef\arraystretch{#1}%
  \hskip -\arraycolsep
  \let\@ifnextchar\new@ifnextchar
  \array{*\c@MaxMatrixCols c}}
\makeatother

% Avoid hbox overfull in the bibliography:
\emergencystretch=1em

% Set bibliography step size
\setlength\bibitemsep{6pt}

% Set white space in lists
\setlist{itemsep=-2pt}

% Increase the space between footnote and text
\setlength{\footnotesep}{9pt}

% Stop footnotes to split across pages:
\interfootnotelinepenalty=10000

% Change the footnote color to primary:
\renewcommand\footnoterule{{\color{primary}\hrule}}

% Change the header color to primary:
\makeatletter
\patchcmd{\headrule}{\hrule}{\color{primary}\hrule}{}{}
\makeatother

% Set the paragraph distance to medskip
\edef\restoreparindent{\parindent=\the\parindent\relax}
\RequirePackage[skip=\medskipamount]{parskip}
\restoreparindent

% Only show sections in TOC
\setcounter{tocdepth}{1}

% Set nomenclature to be 2 columns:
\renewcommand*{\nompreamble}{\begin{multicols}{2}}
\renewcommand*{\nompostamble}{\end{multicols}}
\setlength{\columnsep}{3em}

% Array stretch redef - makes matrices look nicer
\renewcommand{\arraystretch}{1.2}