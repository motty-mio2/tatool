import base64
import pathlib
import re
from typing import Optional, Union

import pandas as pd
import streamlit as st
import streamlit.components.v1 as stc
from PIL import Image, UnidentifiedImageError

current = pathlib.Path(__file__).parent

file = current / "data.csv"
work_dir = pathlib.Path(r"E:\[前期][1T185] ディジタル情報回路-A6回 課題-33084")


def write_csv(data: dict[str, Optional[Union[str, int]]]):
    df = read_csv().append(data, ignore_index=True)  # type:ignore
    df.to_csv(file, mode="w", index=True, encoding="cp932")  # type:ignore


def read_csv() -> pd.DataFrame:
    df = pd.read_csv(file, index_col=0, encoding="cp932")  # type:ignore
    return df


def parse_name() -> Optional[pathlib.Path]:
    df = read_csv()
    for i in work_dir.glob("*onlinetext*"):
        if i.name.split("_")[0] not in df["name"].values:  # type:ignore
            return i


def parse_id(file: pathlib.Path) -> Optional[str]:
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            m = re.search(r"\d{7}[Tt]", line)
            if m is not None:
                txt = m.group()
                return txt.upper()


target = parse_name()

if __name__ == "__main__":
    print(target)
    if target is not None:
        id: Optional[str] = parse_id(target / "onlinetext.html")

        ans_name = target.name.split("_")[0]

        comment = st.text_input(label="コメント", value="")
        score = st.number_input(label="得点", min_value=0, max_value=200, value=0)

        if st.button("採点", key=0):
            # st.session_state["count"] += 1
            write_csv(data={"id": id, "name": ans_name, "score": int(score), "comment": comment})
            target = parse_name()

        if target is not None:
            html = open(target / "onlinetext.html", "r", encoding="utf-8")
            source_code = html.read()
            # source_code = source_code.replace("<p>", "")
            # source_code = source_code.replace("</p>", "")
            source_code = source_code.replace("\n\n", "\n")
            # source_code = source_code.replace('src="', f'src="{target}\\')
            source_code = re.sub("<img.*/>", "", source_code)

            stc.html(source_code, scrolling=True, height=600)

            for img in target.iterdir():
                try:
                    image = Image.open(img)
                    st.image(image, use_column_width=True)
                except UnidentifiedImageError:
                    pass

            img_dir = pathlib.Path(str(target).replace("onlinetext", "file"))

            if img_dir.exists():
                for img in img_dir.iterdir():
                    if "pdf" in img.suffix or "PDF" in img.suffix:
                        with open(img, "rb") as f:
                            base64_pdf = base64.b64encode(f.read()).decode("utf-8")
                        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800"'
                        pdf_display += 'type="application/pdf"></iframe>'
                        st.markdown(pdf_display, unsafe_allow_html=True)
                    else:
                        try:
                            image = Image.open(img)
                            st.image(image, use_column_width=True)
                        except UnidentifiedImageError:
                            pass
        else:
            st.text("finish!")
    else:
        st.text("finish!!")
