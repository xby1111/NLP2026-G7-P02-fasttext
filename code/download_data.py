"""Download a fixed public AG News mirror; no dataset text is bundled."""
import argparse, concurrent.futures, hashlib, pathlib, urllib.request

COMMIT='555590db4219b1243abb1918effd6a7425a2d75f'
FILES={'train.csv':(29470338,'694aa19971315410e000404523796b76349d3c1d'),'test.csv':(1857427,'130b40c3329c993468b8ed8a22c331315e478e0a')}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=pathlib.Path,default=pathlib.Path('data/raw'));p.add_argument('--workers',type=int,default=8);a=p.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    for name,(size,blob) in FILES.items():
        out=a.output/name
        if out.exists():
            data=out.read_bytes()
            if hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob:
                print(name,'verified existing');continue
        base=f'https://raw.githubusercontent.com/mhjabreel/CharCnn_Keras/{COMMIT}/data/ag_news_csv/{name}'
        chunk_size=524288; chunks=a.output/('.chunks_'+name);chunks.mkdir(exist_ok=True)
        def get(i):
            start=i*chunk_size;end=min(size-1,start+chunk_size-1);target=chunks/str(i)
            if target.exists() and target.stat().st_size==end-start+1:return
            for attempt in range(4):
                try:
                    request=urllib.request.Request(base,headers={'Range':f'bytes={start}-{end}','Accept-Encoding':'identity'})
                    with op.open(request,timeout=60) as response:
                        if response.status!=206:raise RuntimeError('Server did not honor byte range')
                        data=response.read()
                    if len(data)!=end-start+1:raise RuntimeError('Incomplete chunk')
                    target.write_bytes(data);print(name,i,'downloaded',flush=True);return
                except Exception:
                    if attempt==3:raise
        count=(size+chunk_size-1)//chunk_size
        with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as pool:list(pool.map(get,range(count)))
        data=b''.join((chunks/str(i)).read_bytes() for i in range(count))
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob,'Source checksum mismatch'
        out.write_bytes(data);print(name,'verified SHA256',hashlib.sha256(data).hexdigest())
if __name__=='__main__':main()
