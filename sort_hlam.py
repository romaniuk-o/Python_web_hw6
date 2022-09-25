import asyncio
import sys
from pathlib import Path
import aioshutil
from aiopath import AsyncPath
from time import time

file_list = []
folder_list = []


async def scan(path: Path) -> None:
    v = Path(path)
    for el in v.iterdir():
        if el.is_dir():
            print(f'Work in folder {el.name}')
            folder_list.append(el)
            await scan(el)
        else:
            file_list.append(el)


async def copy_file(file_path: Path) -> None:
    n = AsyncPath(file_path)
    ext = n.suffix[1:]
    new_path = folder_for_scan / ext.upper()

    try:
        new_path.mkdir()
        print(f'New folder name is {ext}')
    except FileExistsError:
        pass
    await aioshutil.move(n, new_path / n.name)


async def delete_folders(folder: Path) -> None:
    try:
        d = AsyncPath(folder)
        await d.rmdir()
        print(f'Folder {folder} deleted')
    except OSError:
        print(f'Folder {folder} is not deleted')


async def main():
    result = await asyncio.gather(
        *[copy_file(file) for file in file_list],
        *[delete_folders(folder) for folder in folder_list[::-1]]
    )
    return result


if __name__ == '__main__':
    time_ = time()
    folder_for_scan = Path(sys.argv[1])
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    r = loop.run_until_complete(scan(folder_for_scan))
    asyncio.run(main())
    print(time()-time_)
    print('Finish sorting')