
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT

def create_pdf(filename):
    # Professional margins (0.75 inch)
    doc = SimpleDocTemplate(filename, pagesize=letter,
                            rightMargin=54, leftMargin=54,
                            topMargin=54, bottomMargin=54)
    Story = []
    
    styles = getSampleStyleSheet()
    # "Quant Note" Styles
    styles.add(ParagraphStyle(name='QuantTitle', parent=styles['Heading1'], fontSize=16, leading=20, alignment=TA_LEFT, textColor=colors.darkblue))
    styles.add(ParagraphStyle(name='QuantSubtitle', parent=styles['Normal'], fontSize=10, leading=12, alignment=TA_LEFT, textColor=colors.grey))
    styles.add(ParagraphStyle(name='QuantBody', parent=styles['Normal'], fontSize=9, leading=11, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle(name='QuantHeader', parent=styles['Heading3'], fontSize=10, leading=12, spaceBefore=6, spaceAfter=2, textColor=colors.darkblue))
    
    # Header
    Story.append(Paragraph("QUANTITATIVE EQUITY RESEARCH", styles['QuantSubtitle']))
    Story.append(Paragraph("The Presidential Pump: Isolating Alpha in the Pre-Election Year", styles['QuantTitle']))
    Story.append(Paragraph("<b>Author:</b> Gabriel Bengo &nbsp;|&nbsp; <b>Date:</b> December 5, 2024", styles['QuantSubtitle']))
    Story.append(Spacer(1, 12))
    
    # Abstract
    Story.append(Paragraph("<b>ABSTRACT:</b> We investigate the efficiency of the S&P 500 across the 4-year US Presidential Election Cycle (1950-2024). Empirical evidence rejects the 'Election Year' hypothesis in favor of a strong, statistically significant anomaly in the <b>Pre-Election Year (Year 3)</b>, which exhibits a Sharpe Ratio of 1.58 versus the market's 0.57.", styles['QuantBody']))
    Story.append(Spacer(1, 12))
    
    # 1. Investment Thesis
    Story.append(Paragraph("1. INVESTMENT THESIS", styles['QuantHeader']))
    thesis = """
    The 'Political Business Cycle' theory posits that incumbent administrations employ expansionary fiscal and monetary policies in the period substantially preceding an election to maximize economic sentiment during the voting window. Our analysis confirms that this stimulus 'pricing in' occurs primarily in <b>Year 3</b> (Pre-Election), not Year 4.
    """
    Story.append(Paragraph(thesis, styles['QuantBody']))
    
    # 2. Empirical Findings
    Story.append(Paragraph("2. EMPIRICAL FINDINGS (1950-2024)", styles['QuantHeader']))
    Story.append(Paragraph("The performance disparity is structural. Year 3 offers double-digit mean returns with significantly suppressed volatility ($\sigma=10.86\%$).", styles['QuantBody']))
    Story.append(Spacer(1, 6))
    
    # Detailed Data Table
    # Data derived from previous analysis outputs
    # Year 1 (Post): 8.36%, Vol 17.68%
    # Year 2 (Midterm): 3.68%, Vol 20.37%
    # Year 3 (Pre): 17.18%, Vol 10.86%
    # Year 4 (Election): 8.11%, Vol 14.41%
    
    data = [
        ['Cycle Phase', 'Mean Rtn', 'Volatility', 'Sharpe', 'Max DD', 'Win Rate'],
        ['Year 1: Post-Election', '8.36%', '17.68%', '0.47', '-17.37%', '—'],
        ['Year 2: Midterm', '3.68%', '20.37%', '0.18', '-29.72%', '—'],
        ['Year 3: Pre-Election', '17.18%', '10.86%', '1.58', '-0.73%', '89%'],
        ['Year 4: Election', '8.11%', '14.41%', '0.56', '-38.49%', '—'],
        ['Benchmark (Buy & Hold)', '9.41%', '16.57%', '0.57', '-41.92%', '73%']
    ]
    
    t = Table(data, colWidths=[140, 60, 60, 50, 60, 60])
    t.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 8),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue), # Header
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.lightgrey),
        
        # Highlight Year 3
        ('BACKGROUND', (0,3), (-1,3), colors.lightyellow), 
        ('FONTNAME', (0,3), (-1,3), 'Helvetica-Bold'),
        ('BOX', (0,3), (-1,3), 1, colors.black),
    ]))
    Story.append(t)
    
    # 3. Statistical Validity
    Story.append(Paragraph("3. STATISTICAL VALIDITY", styles['QuantHeader']))
    stats_text = """
    We test the null hypothesis $H_0: \mu_{Year3} \le \mu_{Other}$ using a one-tailed Welch's t-test.
    <br/>&bull; T-Statistic: 3.0532
    <br/>&bull; P-Value: 0.0018 ($< 0.01$)
    <br/><br/><b>Conclusion:</b> The outperformance is statistically significant at the 99% confidence level.
    """
    Story.append(Paragraph(stats_text, styles['QuantBody']))
    
    # 4. Strategy & Implementation
    Story.append(Paragraph("4. STRATEGY IMPLICATION", styles['QuantHeader']))
    strat_text = """
    A rigorous 'Year 3 Only' strategy (Cash in Years 1, 2, 4) yields a Max Drawdown of just <b>-0.73%</b> over 75 years, compared to -41.92% for Buy & Hold. This risk profile suggests Year 3 is an ideal window for leveraged exposure or aggressive factor rotation.
    <br/><br/>
    <b>Recommendation:</b> Overweight US Equities (SPY) aggressively at the start of the Pre-Election Year. Neutralize or hedge exposure entering the Election Year.
    """
    Story.append(Paragraph(strat_text, styles['QuantBody']))
    
    # Footer disclaimer
    Story.append(Spacer(1, 24))
    disclaimer = "<b>DISCLAIMER:</b> Past performance is not indicative of future results. Quantitative models are subject to regime change risk."
    Story.append(Paragraph(disclaimer, ParagraphStyle('Disclaimer', parent=styles['Normal'], fontSize=6, textColor=colors.grey)))

    doc.build(Story)
    print(f"PDF generated: {filename}")

if __name__ == "__main__":
    create_pdf("Pre_Election_Alpha_Paper.pdf")
