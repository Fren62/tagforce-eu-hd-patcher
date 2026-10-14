// Windows only: embeds product name and version in the .exe (needed by code signing and shown in the file properties).
fn main() {
    #[cfg(windows)]
    {
        let mut res = winresource::WindowsResource::new();
        res.set("ProductName", "Tag Force EU HD patcher");
        res.set("FileDescription", "Yu-Gi-Oh! GX Tag Force 1 EU HD & text-fix patcher");
        res.set("LegalCopyright", "MIT licence");
        if let Err(e) = res.compile() {
            println!("cargo:warning=could not embed the version resource: {e}");
        }
    }
}
