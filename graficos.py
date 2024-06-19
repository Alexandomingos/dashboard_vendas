import plotly.express as px
from controller.utils import df_rec_forma_pagamento, df_rec_mensal, df_rec_produtos, df_rec_categoria

grafico_coluna_forma_pagamento = px.bar(df_rec_forma_pagamento, x='valor', y='forma_de_pagamento')

grafico_rec_mensal = px.line(df_rec_mensal, 
                            x='Mes', 
                            y='valor', 
                            markers=True, 
                            range_y=(0,df_rec_mensal.max()),
                            color = 'Ano',
                            line_dash= 'Ano',
                            title= 'Receita Mensal'
)

grafico_rec_mensal.update_layout(yaxis_title = 'Receita')

grafico_rec_produto = px.bar(df_rec_produtos.head(7),
                        
                            text_auto=True,
                            orientation='h',
                            title='Top por produto'
    )


grafico_rec_categoria = px.bar(df_rec_categoria.head(7),
                            text_auto=True,
                            title='Top 7 Categoria por Receita'
    )
