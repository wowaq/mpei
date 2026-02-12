from IPython.display import HTML, display

def show_large_number(number_str, description="Число"):
    """Компактное отображение числа с нумерацией десятичных разрядов"""
    
    parts = number_str.split('.')
    integer_part = parts[0].strip()
    decimal_part = parts[1].strip() if len(parts) > 1 else ''
    
    # Генерируем десятичные разряды с номерами
    decimal_digits = ''.join([
        f'<div style="display:inline-flex; flex-direction:column; align-items:center; margin:0 0.5px;">'
        f'<span style="font-size:16px; font-weight:bold; padding:0px 4px; border-radius:4px; color:#fff;">{d}</span>'
        f'<span style="font-size:11px; color:#333; margin-top:1px;">{i}</span>'
        f'</div>'
        for i, d in enumerate(decimal_part, 1)
    ])
    integer_digits = ''.join([
        f'<div style="display:inline-flex; flex-direction:column; align-items:center; margin:0 0.5px;">'
        f'<span style="font-size:16px; font-weight:bold; padding:0px 4px; border-radius:4px; color:#fff;">{d}</span>'
        f'<span style="font-size:11px; color:#333; margin-top:1px;">{i}</span>'
        f'</div>'
        for i, d in enumerate(integer_part, 1)
    ])

    
    
    html = f'''
    <div style="
        background: transparent;
        padding: 2px 2px;
        # border-radius:10px;
        # border-left:4px solid #00f;
        font-family:monospace;
        margin:0px 0;
        box-shadow:0 2px 8px rgba(0,0,0,0.5);
    ">
        <div style="color:#fff; font-size:13px; margin-bottom:2px;">
            {description}
        </div>
        
        <div style="
            background: transparent;
            padding:0 0;
            border-radius:8px;
            overflow-x:auto;
            white-space:nowrap;
        ">
            <span style="font-size:16px; font-weight:bold; color:#fff;">{integer_digits}</span>
            <span style="font-size:16px; font-weight:bold; color:#fff; margin:0 0px;">.</span>
            {decimal_digits}
        </div>
    </div>
    '''
    
    return HTML(html)
