FROM python:3.10.8-bullseye

WORKDIR /app

COPY ./dataviz_charts /app/dataviz_charts
COPY ./.streamlit /root/.streamlit

RUN pip install pandas scikit-learn plotly jupyter notebook streamlit openpyxl currencyconverter yfinance kaleido clickhouse_connect streamlit_pdf_viewer

ENV STREAMLIT_WELCOME_MESSAGE_DISABLED=true
ENV STREAMLIT_DISABLE_PROMPT="true"
EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "dataviz_charts/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
