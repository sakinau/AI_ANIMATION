import { access, mkdir, readFile, writeFile } from "node:fs/promises";
import { createWriteStream } from "node:fs";
import { dirname, join } from "node:path";
import { pipeline } from "node:stream/promises";

const root = "D:/短剧/素材/沙雕动画素材网";
const categories = [
  { id: 12, name: "人物" },
  { id: 14, name: "表情" },
];
const selectedCategoryId = process.argv[2] ? Number(process.argv[2]) : null;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

function sanitizeName(value) {
  return String(value || "未命名")
    .replace(/[\\/:*?"<>|]/g, "_")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 80);
}

async function fetchText(url) {
  const response = await fetch(url, {
    headers: {
      "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36",
      referer: "https://www.qudonghua.com/",
    },
  });
  if (!response.ok) throw new Error(`${response.status} ${url}`);
  return await response.text();
}

function absoluteUrl(url) {
  return new URL(url.replaceAll("&amp;", "&"), "https://www.qudonghua.com/").href;
}

function extractTitle(html) {
  const h1 = html.match(/<h1[^>]*>([\s\S]*?)<\/h1>/i)?.[1];
  const title = h1 || html.match(/<title[^>]*>([\s\S]*?)<\/title>/i)?.[1] || "";
  return title.replace(/<[^>]*>/g, "").replace(/沙雕动画素材[\s\S]*$/g, "").trim();
}

function extractDetailLinks(html, categoryId) {
  const links = new Map();
  const re = /href=["']([^"']*\/show\/(\d+)_(\d+)\/?[^"']*)["'][^>]*>([\s\S]*?)<\/a>/gi;
  for (const match of html.matchAll(re)) {
    const id = `${match[2]}_${match[3]}`;
    const text = match[4].replace(/<[^>]*>/g, "").trim();
    if (text && text !== "多图") {
      links.set(id, { id, title: text, url: absoluteUrl(match[1]) });
    } else if (!links.has(id)) {
      links.set(id, { id, title: "", url: absoluteUrl(match[1]) });
    }
  }
  return [...links.values()];
}

function extractMaxPage(html, categoryId) {
  let max = 1;
  const re = new RegExp(`(?:/sd/class/${categoryId}/)?(\\d+)\\.html`, "g");
  for (const match of html.matchAll(re)) max = Math.max(max, Number(match[1]));
  return max;
}

function extractImages(html) {
  const images = new Map();
  const tagRe = /<img\b[^>]*>/gi;
  const urlRe = /\b(?:src|load)=["']([^"']+)["']/gi;
  for (const tag of html.matchAll(tagRe)) {
    for (const urlMatch of tag[0].matchAll(urlRe)) {
      const url = absoluteUrl(urlMatch[1]);
      if (/^https:\/\/file1(?:-view)?\.qudonghua\.com\/.+\.(?:png|jpe?g|webp|gif)(?:\?.*)?$/i.test(url)) {
        images.set(url, url);
      }
    }
  }
  return [...images.values()];
}

function extensionFromUrl(url) {
  const path = new URL(url).pathname;
  return path.match(/\.(png|jpe?g|webp|gif)$/i)?.[0].toLowerCase() || ".bin";
}

async function downloadFile(url, path) {
  await mkdir(dirname(path), { recursive: true });
  try {
    await access(path);
    return;
  } catch {
    // Missing file, download it.
  }
  const response = await fetch(url, {
    headers: {
      "user-agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36",
      referer: "https://www.qudonghua.com/",
    },
  });
  if (!response.ok) throw new Error(`${response.status} ${url}`);
  await pipeline(response.body, createWriteStream(path));
}

async function main() {
  const manifestPath = join(root, "manifest.json");
  let manifest = [];
  if (selectedCategoryId) {
    try {
      manifest = JSON.parse(await readFile(manifestPath, "utf8"));
      const selectedName = categories.find((category) => category.id === selectedCategoryId)?.name;
      manifest = selectedName ? manifest.filter((row) => row.category !== selectedName) : manifest;
    } catch {
      manifest = [];
    }
  }

  for (const category of categories.filter((item) => !selectedCategoryId || item.id === selectedCategoryId)) {
    const firstUrl = `https://www.qudonghua.com/sd/class/${category.id}/`;
    const firstHtml = await fetchText(firstUrl);
    const maxPage = extractMaxPage(firstHtml, category.id);
    const detailMap = new Map();

    for (let page = 1; page <= maxPage; page++) {
      const url = page === 1 ? firstUrl : `https://www.qudonghua.com/sd/class/${category.id}/${page}.html`;
      const html = page === 1 ? firstHtml : await fetchText(url);
      for (const detail of extractDetailLinks(html, category.id)) detailMap.set(detail.id, detail);
      console.log(`${category.name} 列表 ${page}/${maxPage}: 累计 ${detailMap.size}`);
      await sleep(120);
    }

    const details = [...detailMap.values()];
    for (let index = 0; index < details.length; index++) {
      const detail = details[index];
      const html = await fetchText(detail.url);
      const title = sanitizeName(detail.title || extractTitle(html) || detail.id);
      const images = extractImages(html);
      const folder = join(root, category.name, `${detail.id}_${title}`);

      let downloaded = 0;
      for (let imageIndex = 0; imageIndex < images.length; imageIndex++) {
        const imageUrl = images[imageIndex];
        const ext = extensionFromUrl(imageUrl);
        const filePath = join(folder, `${String(imageIndex + 1).padStart(2, "0")}${ext}`);
        try {
          await downloadFile(imageUrl, filePath);
          downloaded++;
          manifest.push({
            category: category.name,
            id: detail.id,
            title,
            pageUrl: detail.url,
            imageUrl,
            filePath,
          });
          await sleep(80);
        } catch (error) {
          console.error(`下载失败: ${imageUrl} -> ${error.message}`);
        }
      }
      console.log(`${category.name} 详情 ${index + 1}/${details.length}: ${title} (${downloaded}/${images.length})`);
      await sleep(120);
    }
  }

  await mkdir(root, { recursive: true });
  await writeFile(manifestPath, JSON.stringify(manifest, null, 2), "utf8");
  const csv = ["category,id,title,pageUrl,imageUrl,filePath"]
    .concat(
      manifest.map((row) =>
        [row.category, row.id, row.title, row.pageUrl, row.imageUrl, row.filePath]
          .map((value) => `"${String(value).replaceAll('"', '""')}"`)
          .join(",")
      )
    )
    .join("\n");
  await writeFile(join(root, "manifest.csv"), csv, "utf8");
  console.log(`完成: ${manifest.length} 个公开图片素材，保存到 ${root}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
