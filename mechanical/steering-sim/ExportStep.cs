// Opens SolidWorks files with SolidWorks hidden and saves a STEP copy of them.
// Needs SolidWorks 2026, closed. Windows already has the C# compiler, so build it with:
//
//   set API=C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\api\redist
//   C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe /platform:x64 /out:ExportStep.exe
//       /link:"%API%\SolidWorks.Interop.sldworks.dll" /link:"%API%\SolidWorks.Interop.swconst.dll" ExportStep.cs
//
// Then run:  ExportStep.exe step ..\cad-2026\f26bakfiets_main_asm.SLDASM

using System;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using SolidWorks.Interop.sldworks;
using SolidWorks.Interop.swconst;

static class ExportStep
{
    static int Main(string[] args)
    {
        if (args.Length < 2) { Console.Error.WriteLine("usage: ExportStep <out dir> <files...>"); return 2; }
        if (Process.GetProcessesByName("SLDWORKS").Length > 0)
        {
            Console.Error.WriteLine("SolidWorks is already open. Close it and run this again.");
            return 2;
        }
        string out_dir = Path.GetFullPath(args[0]);
        Directory.CreateDirectory(out_dir);

        SldWorks sw = Start();
        if (sw == null) return 3;
        sw.Visible = false;
        sw.UserControl = false;
        int failures = 0;
        try
        {
            for (int i = 1; i < args.Length; i++)
                if (!Export(sw, Path.GetFullPath(args[i]), out_dir)) failures++;
        }
        finally
        {
            sw.CloseAllDocuments(true);
            sw.ExitApp();
            Marshal.ReleaseComObject(sw);
        }
        return failures == 0 ? 0 : 1;
    }

    static bool Export(SldWorks sw, string path, string out_dir)
    {
        int type = path.EndsWith(".SLDASM", StringComparison.OrdinalIgnoreCase)
            ? (int)swDocumentTypes_e.swDocASSEMBLY : (int)swDocumentTypes_e.swDocPART;
        int errors = 0, warnings = 0;
        ModelDoc2 doc = (ModelDoc2)sw.OpenDoc6(path, type,
            (int)swOpenDocOptions_e.swOpenDocOptions_Silent | (int)swOpenDocOptions_e.swOpenDocOptions_ReadOnly,
            "", ref errors, ref warnings);
        if (doc == null)
        {
            Console.Error.WriteLine("Could not open " + path + " (error " + errors + ")");
            return false;
        }
        if (type == (int)swDocumentTypes_e.swDocASSEMBLY)
        {
            ((AssemblyDoc)doc).ResolveAllLightWeightComponents(false);
            object[] comps = (object[])((AssemblyDoc)doc).GetComponents(false);
            Console.WriteLine(Path.GetFileName(path) + ": " + (comps == null ? 0 : comps.Length) + " components");
            if (comps != null)
                foreach (object o in comps)
                {
                    Component2 c = (Component2)o;
                    string state = c.IsSuppressed() ? " (suppressed)" : "";
                    Console.WriteLine("  " + c.Name2 + state + "  <- " + Path.GetFileName(c.GetPathName()));
                }
        }
        doc.ForceRebuild3(false);
        string step = Path.Combine(out_dir, Path.GetFileNameWithoutExtension(path) + ".step");
        bool ok = doc.Extension.SaveAs3(step, (int)swSaveAsVersion_e.swSaveAsCurrentVersion,
            (int)swSaveAsOptions_e.swSaveAsOptions_Silent | (int)swSaveAsOptions_e.swSaveAsOptions_Copy,
            null, null, ref errors, ref warnings);
        Console.WriteLine((ok ? "Saved " : "Could not save ") + step);
        sw.CloseDoc(doc.GetTitle());
        return ok;
    }

    static SldWorks Start()
    {
        var info = new ProcessStartInfo(@"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SLDWORKS.exe");
        info.WindowStyle = ProcessWindowStyle.Minimized;
        Process proc = Process.Start(info);
        DateTime give_up = DateTime.Now.AddMinutes(4);
        while (DateTime.Now < give_up && !proc.HasExited)
        {
            try
            {
                SldWorks sw = (SldWorks)Marshal.GetActiveObject("SldWorks.Application");
                if (sw != null && sw.StartupProcessCompleted) return sw;
            }
            catch (COMException) { }
            System.Threading.Thread.Sleep(2000);
        }
        Console.Error.WriteLine("SolidWorks did not start.");
        return null;
    }
}
