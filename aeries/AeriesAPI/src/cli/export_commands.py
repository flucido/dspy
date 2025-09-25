import click
from src.services.aeries_service import AeriesService
from src.services.formatting_service import FormattingService
from src.services.export_service import ExportService

@click.command()
@click.option('--format', type=click.Choice(['csv', 'excel', 'pdf']), default='csv', help='Export format')
@click.option('--output', default='output', help='Output file name')
def export_data(format, output):
    """Export student data from Aeries."""
    aeries_service = AeriesService()
    formatting_service = FormattingService()
    export_service = ExportService()
    
    students = aeries_service.get_students()
    formatted_data = formatting_service.format_students(students)
    
    if format == 'csv':
        data = export_service.export_to_csv(formatted_data)
        with open(f"{output}.csv", 'w') as f:
            f.write(data)
    elif format == 'excel':
        data = export_service.export_to_excel(formatted_data)
        with open(f"{output}.xlsx", 'wb') as f:
            f.write(data)
    elif format == 'pdf':
        data = export_service.export_to_pdf(formatted_data)
        with open(f"{output}.pdf", 'wb') as f:
            f.write(data)
    
    click.echo(f"Data exported to {output}.{format}")

if __name__ == '__main__':
    export_data()