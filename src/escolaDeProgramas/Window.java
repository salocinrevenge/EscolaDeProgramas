package escolaDeProgramas;

import java.awt.Dimension;
import javax.swing.JFrame;
import javax.swing.JPanel;

public class Window extends JFrame{
	private static final long serialVersionUID = 1L;
	
	public Window() {
		super("Escola de Programas");
		this.setPreferredSize(new Dimension(1000,500));
		this.setResizable(false);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		//add(desenho);                           
		pack();				       	    
		setVisible(true);
	}
	
}
