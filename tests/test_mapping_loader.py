from pathlib import Path

from src.mappings.load_dim_products import read_mapping_df


def test_read_mapping_df_reads_csv_with_commas(tmp_path):
    mapping_path = tmp_path / "products.csv"
    mapping_path.parent.mkdir(parents=True, exist_ok=True)
    mapping_path.write_text(
        "store,raw_name,clean_name,category,subcategory,product_id,is_food\n"
        "biedronka,Milk,Milk,Dairy,Milk,12345,true\n",
        encoding="utf-8",
    )

    df = read_mapping_df(mapping_path)

    assert not df.empty
    assert list(df.columns)[:3] == ["store", "raw_name", "clean_name"]
    assert df.loc[0, "store"] == "biedronka"
