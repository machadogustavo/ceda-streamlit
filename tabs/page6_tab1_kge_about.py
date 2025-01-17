import streamlit as st
import hydroeval as he
import pandas as pd

def render():
    with st.container():
        st.title("KGE - Eficiência Kling-Gupta")
        
        with st.expander("Sobre o KGE", icon=":material/info:"):
            st.write("""
            **KGE - Eficiência Kling-Gupta** é uma medida estatística usada para avaliar o desempenho de modelos hidrológicos. 
            Ela combina a correlação, a razão de variabilidade e a razão de viés em uma única medida de desempenho do modelo.
            O KGE varia de -∞ a 1, sendo que 1 indica uma concordância perfeita entre o modelo e os dados observados.
            """)
            
            st.latex(r'''
            KGE(y, \hat{y}) = 1 - \sqrt{
                \left( r(y, \hat{y}) - 1 \right)^2
                + \left( \beta(y, \hat{y}) - 1 \right)^2
                + \left( \gamma(y, \hat{y}) - 1 \right)^2
            }
            ''')
            
            st.caption("Legenda")
            
            st.markdown("""
                        - r = coeficiente de correlação
                        - α = razão de variabilidade
                        - β = razão de viés
                        - $\mu$ = média
                        - $\sigma$ = desvio padrão
                        """)

        with st.expander("Tipos de KGE", icon=":material/list:"):
            st.write("""
                - **KGE Original**: Considera a correlação (r), a razão de variabilidade (α) e a razão de viés (β).
                - **KGE Modificado (KGE')**: Substitui α pela razão do coeficiente de variação (γ).
                - **KGE Não-Paramétrico (KGEnp)**: Usa a correlação de postos de Spearman no lugar da de Pearson e ajusta o cálculo para variabilidade e viés.
            """)

        st.subheader("Exemplo de Cálculo do KGE")

        st.write("""
        Abaixo está um exemplo de como você pode calcular a Eficiência Kling-Gupta utilizando a biblioteca `hydroeval`.
        """)

        with st.expander("Sobre a biblioteca hydroeval", icon=":material/package_2:"):
            st.write("""
            A **hydroeval** é uma ferramenta de código aberto para avaliar a qualidade do ajuste entre séries temporais de fluxo de água simuladas e observadas em Python. 
            Ela é licenciada sob a licença GNU GPL-3.0 e oferece uma série de funções objetivas comumente usadas em ciência hidrológica.
            
            A biblioteca é projetada para calcular essas funções de forma vetorizada (usando numpy, o que acelera os cálculos com código em C nos bastidores), tornando os cálculos muito eficientes.
            
            Funções objetivas disponíveis na **hydroeval** incluem:
            - **NSE (Nash-Sutcliffe Efficiency)**
            - **KGE Original e seus componentes** (r, α, β)
            - **KGE Modificado** (kgeprime) e seus componentes (r, γ, β)
            - **KGE Não-Paramétrico** (kgenp) e seus componentes (r, α, β)
            - **RMSE (Root Mean Square Error)**
            - **MARE (Mean Absolute Relative Error)**
            - **PBIAS (Percent Bias)**
            """)

        simulacoes = [5.3, 4.2, 5.7, 2.3]
        avaliacoes = [4.7, 4.3, 5.5, 2.7]

        st.markdown("""        
        ```python
        # Definindo os dados de exemplo
        simulacoes = [5.3, 4.2, 5.7, 2.3]
        avaliacoes = [4.7, 4.3, 5.5, 2.7]

        # Calculando o NSE
        nse = he.evaluator(he.nse, simulacoes, avaliacoes)
        
        # Calculando o KGE
        kge, r, alpha, beta = he.evaluator(he.kge, simulacoes, avaliacoes)

        # Exibindo os resultados
        print(f"NSE: {nse}")
        print(f"KGE: {kge}")
        print(f"Correlação (r): {r}")
        print(f"Razão de Viés (β): {beta}")
        print(f"Razão de Variabilidade (α): {alpha}")
        ```
        """)



        st.subheader("Saída")

        nse = he.evaluator(he.nse, simulacoes, avaliacoes)

        kge, r, alpha, beta = he.evaluator(he.kge, simulacoes, avaliacoes)

        data = {
            "Métrica": ["NSE", "KGE", "Correlação (r)", "Razão de Viés (β)", "Razão de Variabilidade (α)"],
            "Valor": [nse, kge, r, beta, alpha]
        }
        df = pd.DataFrame(data)
        st.table(df)

        st.subheader("Resultado")
        st.write("""
        - O **NSE** (Eficiência de Nash-Sutcliffe) tem um valor de **0.8629**, o que sugere que o modelo é bastante eficiente, já que valores próximos a 1 indicam um bom ajuste entre as simulações e as avaliações.
        - O **KGE** (Eficiência Kling-Gupta) tem um valor de **0.7066**, indicando uma boa concordância entre o modelo e os dados observados. No entanto, um valor mais alto (próximo de 1) indicaria uma correspondência melhor.
        - A **Correlação (r)** de **0.9821** é bastante alta, o que significa que as simulações e avaliações estão bem relacionadas em termos de tendência.
        - A **Razão de Viés (β)** de **1.0174** indica que há um leve viés, já que valores próximos a 1 representam um modelo com pouca ou nenhuma tendência de superestimar ou subestimar os valores.
        - A **Razão de Variabilidade (α)** de **1.2923** sugere que a variabilidade do modelo é um pouco maior que a variabilidade observada, já que valores próximos a 1 indicam boa concordância na variabilidade.
        """)


        st.divider()

        st.subheader("Fonte:")
        st.markdown("""
                    - [KGE - Kling-Gupta Efficiency — Permetrics 2.0.0 documentation](https://permetrics.readthedocs.io/en/latest/pages/regression/KGE.html) 
                    - [Hydroeval - PyPI](https://pypi.org/project/hydroeval/) 
                    - [DOI oficial](https://doi.org/10.5281/zenodo.2591217)
                    """)