import os

def split_file(file_path, chunk_size=1024 * 1024):  # Default: 1MB chunks
    chunks = []
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)

    with open(file_path, 'rb') as f:
        i = 0
        while chunk := f.read(chunk_size):
            chunk_name = f"{name}_chunk{i:04d}{ext}"  # e.g., resume_chunk0000.pdf
            chunks.append((chunk_name, chunk))
            i += 1

    return chunks

def save_chunk(chunk_name, data, node_path):
    os.makedirs(node_path, exist_ok=True)
    with open(os.path.join(node_path, chunk_name), 'wb') as f:
        f.write(data)

def assemble_file(chunks):
    # Sort chunks based on numeric index extracted from filename
    def extract_index(name):
        parts = name.split("_chunk")
        if len(parts) > 1:
            return int(parts[1].split(".")[0])
        return 0

    chunks.sort(key=lambda x: extract_index(x[0]))
    return b''.join(chunk for _, chunk in chunks)
