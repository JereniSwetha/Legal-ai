export default function FileUpload({ onFileSelect }) {
  const handleChange = (e) => {
    const file = e.target.files[0];
    if (file) onFileSelect(file);
  };

  return (
    <div>
      <input type="file" onChange={handleChange} />
    </div>
  );
}
