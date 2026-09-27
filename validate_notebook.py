"""Execute the notebook from scratch and verify the app analysis and charts."""
from pathlib import Path
import sys
import nbformat
from nbclient import NotebookClient
from jupyter_client import KernelManager

root = Path(__file__).resolve().parent
nb = nbformat.read(root / "notebook.ipynb", as_version=4)
nbformat.validate(nb)
for cell in nb.cells:
    if cell.cell_type == "code":
        cell.outputs = []
        cell.execution_count = None
nb.cells.append(nbformat.v4.new_code_cell("\nassert len(apps) == 9659 and apps.App.is_unique\nassert apps.Category.nunique() == 33\nassert len(rated) == 8196 and apps.Rating.isna().sum() == 1463\nassert rated.Rating.between(1,5).all()\nassert apps.Installs.ge(0).all() and apps.Price.ge(0).all()\nassert apps.loc[apps.Type.eq('Free'), 'Price'].eq(0).all()\nassert paid.Price.gt(0).all()\nassert int(category_counts.sum()) == len(apps)\nassert int(install_summary.Apps.sum()) == len(apps)\nassert clean_apps(raw_apps).equals(apps)\nfixture = raw_apps.head(2).copy()\nfixture.loc[fixture.index[0], 'Installs'] = '1,000+'\nfixture.loc[fixture.index[0], 'Price'] = '$2.99'\ncleaned = clean_apps(fixture)\nassert cleaned.iloc[0].Installs == 1000 and cleaned.iloc[0].Price == 2.99\nassert len(raw_reviews) == 64295\nassert not reviews.duplicated().any()\nassert len(joined) == len(reviews)\nassert len(matched) + joined['_merge'].eq('left_only').sum() == len(reviews)\nassert matched.Sentiment_Polarity.between(-1,1).all()\nassert set(matched.Sentiment).issubset({'Positive', 'Negative', 'Neutral'})\nassert matched[['Review','Sentiment','Sentiment_Polarity','Type']].notna().all().all()\nassert int(review_summary.Reviews.sum()) == len(matched)\nassert int(app_polarity.Review_rows.sum()) == len(matched)\nassert app_polarity.App.is_unique\nassert len(size_rated) == apps[['Size','Rating']].notna().all(axis=1).sum()\nfor file in ['categories_and_ratings.png','size_and_price.png','install_bands.png','review_sentiment.png']:\n    assert Path(file).is_file() and Path(file).stat().st_size > 10000\nprint('PASS: data integrity, numeric cleaning, missing values, review joins and chart outputs')\n"))
km = KernelManager(kernel_name="python3")
km.kernel_spec.argv = [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"]
client = NotebookClient(nb, km=km, timeout=180,
    resources={"metadata": {"path": str(root)}})
try:
    client.execute()
finally:
    if km.has_kernel:
        km.shutdown_kernel(now=True)
nb.cells.pop()
nbformat.write(nb, root / "notebook.ipynb")
print("PASS: notebook executed from cleared outputs; app-analysis and chart checks passed.")
